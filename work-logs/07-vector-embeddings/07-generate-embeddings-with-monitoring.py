# =================================================================================================
# File:          07-generate-embeddings-with-monitoring.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Generate sentence embeddings for application descriptions and reviews with live CPU/RAM/GPU
#   telemetry, writing vectors back into PostgreSQL. Designed for long, resumable runs on GPU nodes.
#
# Section Map:
#   1) Imports                         — dependencies and why they’re needed
#   2) Configuration & Logging         — .env, warnings, rotating/stream logs
#   3) SystemMonitor (Core Component)  — background thread for host/GPU stats
#   4) EmbeddingGenerator (Core)       — model init, DB I/O, adaptive encoding
#   5) CLI / Entry Point               — parse args → run generator
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: PostgreSQL (tables: applications, reviews, embedding_runs)
#   READS:           applications.combined_text, reviews.review_text
#   WRITES:          applications.description_embedding, reviews.review_embedding, embedding_runs.*
#
# Security:
#   - Secrets from .env (PG_HOST, PG_PORT, PG_APP_USER, PG_APP_USER_PASSWORD).
#   - No PII is created; text originates from Steam public pages.
#
# Change Log (docs-only):
#   - 2025-09-29  Standardized header + dual-audience inline comments; no code changes.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: torch for CUDA; psycopg2 for Postgres; sentence-transformers for embeddings; psutil/pynvml for stats.
# ML:    DEPENDS_ON = ["torch","psycopg2","sentence-transformers","python-dotenv","tqdm","psutil","pynvml","numpy (runtime)"]
import os
import sys
import torch
import logging
import argparse
import psycopg2
import threading
import time
import warnings
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from tqdm import tqdm
import psutil
import pynvml
import io

# --- Configuration & Logging ----------------------------------------------------------------------
# Human: silence pynvml deprecation warning; load env; file+console logging for long runs.
# ML:    CONFIG_KEYS = ["PG_HOST","PG_PORT","PG_APP_USER","PG_APP_USER_PASSWORD"]
warnings.filterwarnings("ignore", message="The pynvml package is deprecated.")
load_dotenv()

log_filename = f"embedding_run_{time.strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

# --- Core Component -------------------------------------------------------------------------------
# Human: background sampler for host + GPU metrics; runs as daemon so it won’t block shutdown.
# ML:    CONTRACT: start() -> thread alive; get_stats() -> dict; format_stats(dict) -> str
class SystemMonitor:
    def __init__(self, interval=30):
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)
        try:
            pynvml.nvmlInit()
            self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.has_gpu = True
        except pynvml.NVMLError:
            logging.warning("NVIDIA GPU not found or pynvml failed. GPU stats will not be monitored.")
            self.has_gpu = False

    def get_stats(self):
        stats = {
            "cpu_percent": psutil.cpu_percent(), "ram_percent": psutil.virtual_memory().percent,
            "gpu_util_percent": None, "gpu_mem_percent": None, "gpu_temp_c": None
        }
        if self.has_gpu:
            try:
                utilization = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
                memory = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
                stats.update({
                    "gpu_util_percent": utilization.gpu,
                    "gpu_mem_percent": round(100 * memory.used / memory.total, 2),
                    "gpu_temp_c": pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
                })
            except pynvml.NVMLError as e:
                logging.warning(f"Could not poll GPU stats: {e}")
                self.has_gpu = False
        return stats

    def format_stats(self, stats):
        cpu = f"CPU: {stats['cpu_percent']}%"
        ram = f"RAM: {stats['ram_percent']}%"
        if self.has_gpu and stats['gpu_util_percent'] is not None:
            gpu = f"GPU: {stats['gpu_util_percent']}% | Mem: {stats['gpu_mem_percent']}% | Temp: {stats['gpu_temp_c']}°C"
            return f"{cpu} | {ram} | {gpu}"
        return f"{cpu} | {ram}"
    
    def run(self):
        while not self.stop_event.is_set():
            stats = self.get_stats()
            logging.info(f"STATS - {self.format_stats(stats)}")
            time.sleep(self.interval)

    def start(self): self.thread.start()
    def stop(self):
        self.stop_event.set()
        if self.has_gpu: pynvml.nvmlShutdown()

# --- Core Component -------------------------------------------------------------------------------
# Human: wraps model + DB; performs chunked reads and adaptive-batch encoding; updates vectors in-place.
# ML:    CONTRACT(process_table): (table,id_col,text_col,vector_col,id_type) -> writes vectors; updates embedding_runs
class EmbeddingGenerator:
    def __init__(self, db_name, model_name, batch_size, processing_chunk_size=10000):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.batch_size = batch_size
        self.processing_chunk_size = processing_chunk_size

        logging.info(f"Initializing model '{self.model_name}' on device '{self.device}'.")
        self.model = SentenceTransformer(self.model_name, device=self.device, trust_remote_code=True)
        self.model.max_seq_length = 8192
        self.dimension = self.model.get_sentence_embedding_dimension()

        self.conn_config = {'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name, 'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')}
        self.conn = psycopg2.connect(**self.conn_config)
        self.run_id = self._get_or_create_run_id()
        self.monitor = SystemMonitor()

    def _get_or_create_run_id(self):
        # Human: one row per (model, dimension, normalized) tuple; reuses existing row to keep lineage compact.
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO embedding_runs (model_name, dimension, normalized) VALUES (%s, %s, %s) "
                "ON CONFLICT (model_name, dimension, normalized) DO UPDATE SET model_name = EXCLUDED.model_name "
                "RETURNING run_id;",
                (self.model_name, self.dimension, True)
            )
            run_id = cur.fetchone()[0]
            self.conn.commit()
            logging.info(f"Using embedding run ID: {run_id} for model '{self.model_name}'.")
            return run_id

    def _embed_texts(self, texts, current_batch_size):
        """Encodes texts with adaptive batching for OOM errors."""
        try:
            return self.model.encode(texts, batch_size=current_batch_size, normalize_embeddings=True,
                                     convert_to_numpy=True, show_progress_bar=False)
        except torch.cuda.OutOfMemoryError:
            # Human: halve batch and recurse; base case=1 to surface the error.
            if current_batch_size <= 1:
                logging.error("CUDA OutOfMemoryError even with batch size of 1. Cannot proceed.")
                raise
            
            logging.warning(f"CUDA OutOfMemoryError with batch size {current_batch_size}. Halving and retrying.")
            torch.cuda.empty_cache()
            
            new_batch_size = max(1, current_batch_size // 2)
            # Recursively retry with smaller batches
            embeddings1 = self._embed_texts(texts[:len(texts)//2], new_batch_size)
            embeddings2 = self._embed_texts(texts[len(texts)//2:], new_batch_size)
            return np.vstack([embeddings1, embeddings2])


    def process_table(self, table, id_col, text_col, vector_col, id_type='BIGINT'):
        logging.info(f"--- Starting embedding generation for table: {table} ---")
        where_clause = f"WHERE {text_col} IS NOT NULL AND {vector_col} IS NULL"
        
        # Human: count upfront for progress bars; avoids scanning inside loop.
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table} {where_clause}")
            total_records = cur.fetchone()[0]

        if total_records == 0:
            logging.info(f"No records to process for table '{table}'. Skipping.")
            return

        with tqdm(total=total_records, desc=f"Embedding {table}", unit=" records") as pbar:
            offset = 0
            # Human: OFFSET pagination can degrade on large tables but is simple; acceptable for first pass.
            while offset < total_records:
                with self.conn.cursor() as cur:
                    cur.execute(f"SELECT {id_col}, {text_col} FROM {table} {where_clause} "
                                f"ORDER BY {id_col} LIMIT {self.processing_chunk_size} OFFSET {offset}")
                    chunk = cur.fetchall()

                if not chunk: break

                ids, texts = zip(*chunk)
                vectors = self._embed_texts(texts, self.batch_size)
                
                # Human: free VRAM between large batches to reduce fragmentation.
                if self.device == "cuda":
                    torch.cuda.empty_cache()

                # Human: temp table + COPY for bulk update; avoids per-row UPDATE overhead.
                temp_table_name = f"temp_embedding_update_{table}"
                with self.conn.cursor() as cur:
                    cur.execute(f"CREATE TEMP TABLE {temp_table_name} (id {id_type}, embedding vector({self.dimension})) ON COMMIT DROP;")
                    sio = io.StringIO()
                    for i, vec in zip(ids, vectors):
                        sio.write(f"{i}\t{vec.tolist()}\n")
                    sio.seek(0)
                    cur.copy_expert(f"COPY {temp_table_name} (id, embedding) FROM STDIN", sio)

                    cur.execute(
                        f"""
                        UPDATE {table} t
                        SET 
                            {vector_col} = tmp.embedding,
                            embedding_run_id = %s
                        FROM {temp_table_name} tmp
                        WHERE t.{id_col} = tmp.id
                        """, (self.run_id,)
                    )
                self.conn.commit()

                offset += len(chunk)
                pbar.update(len(chunk))
                pbar.set_postfix_str(self.monitor.format_stats(self.monitor.get_stats()))
                
        logging.info(f"--- Finished embedding generation for table: {table} ---")

    def run(self):
        # Human: monitor runs alongside embedding to surface resource pressure in logs.
        self.monitor.start()
        try:
            self.process_table('applications', 'appid', 'combined_text', 'description_embedding', id_type='BIGINT')
            self.process_table('reviews', 'recommendationid', 'review_text', 'review_embedding', id_type='TEXT')
        finally:
            self.monitor.stop()
            self.conn.close()
            logging.info("🎉 Embedding generation complete. Database connection closed.")

# --- Orchestration / CLI --------------------------------------------------------------------------
# Human: simple CLI for model + batch size; DB name is positional for flexibility (prod vs dev DB).
# ML:    ENTRYPOINT(main): args -> EmbeddingGenerator(db, model, batch) -> run()
def main():
    parser = argparse.ArgumentParser(description="Generate sentence embeddings for the Steam dataset with system monitoring.")
    parser.add_argument("db_name", help="The name of the target database (e.g., 'steamfull').")
    parser.add_argument("--model", default="BAAI/bge-m3", help="The sentence-transformer model to use.")
    parser.add_argument("--batch_size", type=int, default=16, help="Initial batch size for GPU processing.")
    args = parser.parse_args()
    generator = EmbeddingGenerator(args.db_name, args.model, args.batch_size)
    generator.run()

# --- Entry Point -----------------------------------------------------------------------------------
# Human: numpy is imported here (used in _embed_texts recursion) to keep import cost away from CLI parse.
# ML:    RUNTIME_START — direct execution path.
if __name__ == "__main__":
    import numpy as np
    main()
