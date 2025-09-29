# =================================================================================================
# File:          generate-embeddings-with-monitoring.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Same as the “07-” variant, but optimized to use keyset pagination (no OFFSET) for scalability.
#   Generates embeddings for applications + reviews with live system telemetry and bulk updates.
#
# Notes:
#   - “SURGICAL EDIT” comments in the original file already document the keyset switch; retained as-is.
#
# Section Map:
#   1) Imports  2) Config & Logging  3) SystemMonitor  4) EmbeddingGenerator  5) CLI / Entry
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: PostgreSQL (applications, reviews, embedding_runs)
#   READS/WRITES:    same as the “07-” variant
#
# Security:
#   - Secrets from .env (PG_*). No secrets in code.
#
# Change Log (docs-only):
#   - 2025-09-29  Standardized header + inline commentary; preserved keyset pagination logic.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
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
# Human: compared to the “07-” version, this uses keyset pagination via `last_id` instead of OFFSET.
# ML:    CONTRACT(process_table): identical side effects; lower latency on large tables.
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
        
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {text_col} IS NOT NULL AND {vector_col} IS NULL")
            total_records = cur.fetchone()[0]

        if total_records == 0:
            logging.info(f"No records to process for table '{table}'. Skipping.")
            return

        # ==================== SURGICAL EDIT START ====================
        # Human: keyset pagination avoids large OFFSET scans; initialize last seen ID based on type.
        last_id = 0 if id_type == 'BIGINT' else ''
        # ===================== SURGICAL EDIT END =====================

        with tqdm(total=total_records, desc=f"Embedding {table}", unit=" records") as pbar:
            while True: # Loop until no more records are found
                with self.conn.cursor() as cur:
                    # ==================== SURGICAL EDIT START ====================
                    # Human: fetch rows strictly greater than the last ID; keeps the index hot.
                    query = f"""
                        SELECT {id_col}, {text_col} FROM {table}
                        WHERE {id_col} > %s AND {text_col} IS NOT NULL AND {vector_col} IS NULL
                        ORDER BY {id_col}
                        LIMIT {self.processing_chunk_size}
                    """
                    cur.execute(query, (last_id,))
                    # ===================== SURGICAL EDIT END =====================
                    chunk = cur.fetchall()

                if not chunk:
                    pbar.set_description(f"Embedding {table} (Completed)")
                    break # Exit the loop when no more records are returned

                ids, texts = zip(*chunk)
                vectors = self._embed_texts(texts, self.batch_size)

                # ==================== SURGICAL EDIT START ====================
                # Human: set last_id to the last ID in the current chunk to continue keyset pagination.
                last_id = ids[-1]
                # ===================== SURGICAL EDIT END =====================

                if self.device == "cuda":
                    torch.cuda.empty_cache()

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

                pbar.update(len(chunk))
                pbar.set_postfix_str(self.monitor.format_stats(self.monitor.get_stats()))
        
        # Human: ensure the progress bar shows completion when we knew a total upfront.
        if total_records > 0:
            pbar.n = total_records
            pbar.refresh()

        logging.info(f"--- Finished embedding generation for table: {table} ---")

    def run(self):
        self.monitor.start()
        try:
            self.process_table('applications', 'appid', 'combined_text', 'description_embedding', id_type='BIGINT')
            self.process_table('reviews', 'recommendationid', 'review_text', 'review_embedding', id_type='TEXT')
        finally:
            self.monitor.stop()
            self.conn.close()
            logging.info("🎉 Embedding generation complete. Database connection closed.")

# --- Orchestration / CLI --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate sentence embeddings for the Steam dataset with system monitoring.")
    parser.add_argument("db_name", help="The name of the target database (e.g., 'steamfull').")
    parser.add_argument("--model", default="BAAI/bge-m3", help="The sentence-transformer model to use.")
    parser.add_argument("--batch_size", type=int, default=16, help="Initial batch size for GPU processing.")
    args = parser.parse_args()
    generator = EmbeddingGenerator(args.db_name, args.model, args.batch_size)
    generator.run()

# --- Entry Point -----------------------------------------------------------------------------------
if __name__ == "__main__":
    import numpy as np
    main()
