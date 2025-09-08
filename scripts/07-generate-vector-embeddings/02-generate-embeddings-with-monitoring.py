# =====================================================================================================================
# Script Name:    07-generate-embeddings-with-monitoring.py
# Description:    A high-performance script to generate vector embeddings for text data in the PostgreSQL
#                 database using a sentence-transformer model. It is designed for GPU acceleration and
#                 includes features for resilience, such as adaptive batching for out-of-memory errors,
#                 and real-time system monitoring for operational insight during long-running jobs.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.0
# Date:           2025-09-07
# License:        MIT License
#
# Usage:          python 07-generate-embeddings-with-monitoring.py <database_name> --model <model_name> --batch_size <size>
# Example:        python 07-generate-embeddings-with-monitoring.py steamfull --model BAAI/bge-m3 --batch_size 16
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-07      1.0             vintagedon      Initial release of the embedding generation script.
#
# =====================================================================================================================

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
import numpy as np

# --- Configuration ---
# Suppress a known deprecation warning from pynvml to keep logs clean.
warnings.filterwarnings("ignore", message="The pynvml package is deprecated.")
load_dotenv()

# Set up logging to output to both a file and the console for persistent and real-time monitoring.
log_filename = f"embedding_run_{time.strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

# --- System & GPU Monitoring ---
class SystemMonitor:
    """
    A non-blocking system monitor that runs in a separate thread.
    
    Why threading? For a long-running, resource-intensive task like embedding generation,
    it's critical to have out-of-band monitoring. Running this in a separate thread allows us
    to get regular, real-time updates on system health (CPU, RAM, GPU) without interrupting
    the main processing loop. This is a standard pattern for operational tooling.
    """
    def __init__(self, interval=30):
        self.interval = interval
        self.stop_event = threading.Event()
        # The thread is set as a daemon so it will exit automatically when the main program finishes.
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.has_gpu = False
        try:
            # Initialize the NVIDIA Management Library (NVML)
            pynvml.nvmlInit()
            self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.has_gpu = True
        except pynvml.NVMLError:
            logging.warning("NVIDIA GPU not found or pynvml failed. GPU stats will not be monitored.")

    def get_stats(self) -> dict:
        """Polls psutil and pynvml to get current system and GPU metrics."""
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
                self.has_gpu = False # Stop trying if polling fails
        return stats

    def format_stats(self, stats: dict) -> str:
        """Formats the statistics dictionary into a clean, single-line string for logging."""
        cpu = f"CPU: {stats['cpu_percent']}%"
        ram = f"RAM: {stats['ram_percent']}%"
        if self.has_gpu and stats['gpu_util_percent'] is not None:
            gpu = f"GPU: {stats['gpu_util_percent']}% | Mem: {stats['gpu_mem_percent']}% | Temp: {stats['gpu_temp_c']}°C"
            return f"{cpu} | {ram} | {gpu}"
        return f"{cpu} | {ram}"

    def run(self):
        """The main loop for the monitoring thread."""
        while not self.stop_event.is_set():
            stats = self.get_stats()
            logging.info(f"STATS - {self.format_stats(stats)}")
            time.sleep(self.interval)

    def start(self): self.thread.start()
    def stop(self):
        self.stop_event.set()
        if self.has_gpu: pynvml.nvmlShutdown()

# --- Main Embedding Generator Class ---
class EmbeddingGenerator:
    """
    Orchestrates the entire ML pipeline: fetching data from PostgreSQL, generating
    embeddings with a sentence-transformer model, and updating the database.
    """
    def __init__(self, db_name, model_name, batch_size, processing_chunk_size=10000):
        # Auto-detect CUDA availability for GPU acceleration.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.batch_size = batch_size
        # This controls how many records we pull from the database at a time to avoid
        # loading millions of text records into RAM at once.
        self.processing_chunk_size = processing_chunk_size

        logging.info(f"Initializing model '{self.model_name}' on device '{self.device}'.")
        self.model = SentenceTransformer(self.model_name, device=self.device, trust_remote_code=True)
        # Increasing max_seq_length can improve embedding quality for long descriptions,
        # but also increases VRAM usage.
        self.model.max_seq_length = 8192
        self.dimension = self.model.get_sentence_embedding_dimension()

        self.conn_config = {'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name, 'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')}
        self.conn = psycopg2.connect(**self.conn_config)
        # The `run_id` is a critical feature for data lineage and reproducibility. It allows us
        # to track exactly which model version and configuration was used to generate each embedding.
        self.run_id = self._get_or_create_run_id()
        self.monitor = SystemMonitor()

    def _get_or_create_run_id(self) -> int:
        """Gets or creates an entry in the `embedding_runs` table for this specific model configuration."""
        with self.conn.cursor() as cur:
            # INSERT ON CONFLICT is an idempotent way to get an ID for a unique combination of parameters.
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

    def _embed_texts(self, texts: list, current_batch_size: int) -> np.ndarray:
        """
        Encodes a list of texts into embeddings with adaptive batching to handle CUDA Out-of-Memory errors.
        
        This recursive approach is a key resilience feature. If a batch is too large for the GPU's VRAM
        (due to very long texts), instead of crashing, the script will automatically halve the batch
        size and retry, ensuring the process can complete even with highly variable data.
        """
        try:
            return self.model.encode(texts, batch_size=current_batch_size, normalize_embeddings=True,
                                     convert_to_numpy=True, show_progress_bar=False)
        except torch.cuda.OutOfMemoryError:
            if current_batch_size <= 1:
                logging.error("CUDA OutOfMemoryError even with batch size of 1. A text record is likely too long. Cannot proceed with this chunk.")
                raise

            logging.warning(f"CUDA OutOfMemoryError with batch size {current_batch_size}. Halving and retrying.")
            torch.cuda.empty_cache() # Free up cached memory on the GPU.

            new_batch_size = max(1, current_batch_size // 2)
            # Recursively split the batch and process the two halves.
            mid_point = len(texts) // 2
            embeddings1 = self._embed_texts(texts[:mid_point], new_batch_size)
            embeddings2 = self._embed_texts(texts[mid_point:], new_batch_size)
            return np.vstack([embeddings1, embeddings2])

    def process_table(self, table: str, id_col: str, text_col: str, vector_col: str, id_type: str = 'BIGINT'):
        """Processes a single table, fetching records, generating embeddings, and updating the database in chunks."""
        logging.info(f"--- Starting embedding generation for table: {table} ---")
        # The WHERE clause ensures the process is resumable; it only selects records that haven't been processed yet.
        where_clause = f"WHERE {text_col} IS NOT NULL AND {text_col} <> '' AND {vector_col} IS NULL"

        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table} {where_clause}")
            total_records = cur.fetchone()[0]

        if total_records == 0:
            logging.info(f"No records to process for table '{table}'. Skipping.")
            return

        with tqdm(total=total_records, desc=f"Embedding {table}", unit=" records") as pbar:
            offset = 0
            while offset < total_records:
                # Fetch records from the DB in manageable chunks to control RAM usage.
                with self.conn.cursor() as cur:
                    cur.execute(f"SELECT {id_col}, {text_col} FROM {table} {where_clause} "
                                f"ORDER BY {id_col} LIMIT {self.processing_chunk_size} OFFSET {offset}")
                    chunk = cur.fetchall()

                if not chunk: break

                ids, texts = zip(*chunk)
                vectors = self._embed_texts(list(texts), self.batch_size)
                
                if self.device == "cuda": torch.cuda.empty_cache()

                # --- High-Performance Database Update ---
                # Instead of running thousands of individual UPDATE statements, we use a much faster
                # bulk-update pattern. We create a temporary table, use the highly optimized COPY
                # command to load all our new data into it, and then perform a single, fast
                # UPDATE...FROM... command to apply the changes to the main table.
                temp_table_name = f"temp_embedding_update_{table}"
                with self.conn.cursor() as cur:
                    cur.execute(f"CREATE TEMP TABLE {temp_table_name} (id {id_type}, embedding vector({self.dimension})) ON COMMIT DROP;")
                    # Use an in-memory string buffer to prepare data for the COPY command.
                    sio = io.StringIO()
                    for i, vec in zip(ids, vectors):
                        sio.write(f"{i}\t{vec.tolist()}\n")
                    sio.seek(0)
                    cur.copy_expert(f"COPY {temp_table_name} (id, embedding) FROM STDIN", sio)

                    # The single, efficient bulk update operation.
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
                # Update the progress bar with the latest system stats for real-time monitoring.
                pbar.set_postfix_str(self.monitor.format_stats(self.monitor.get_stats()))

        logging.info(f"--- Finished embedding generation for table: {table} ---")

    def run(self):
        """Main execution function for the class."""
        self.monitor.start()
        try:
            # Process each target table sequentially.
            self.process_table('applications', 'appid', 'combined_text', 'description_embedding', id_type='BIGINT')
            self.process_table('reviews', 'recommendationid', 'review_text', 'review_embedding', id_type='TEXT')
        finally:
            self.monitor.stop()
            self.conn.close()
            logging.info("🎉 Embedding generation complete. Database connection closed.")

def main():
    """Parses command-line arguments and kicks off the embedding generation process."""
    parser = argparse.ArgumentParser(description="Generate sentence embeddings for the Steam dataset with system monitoring.")
    parser.add_argument("db_name", help="The name of the target database (e.g., 'steamfull').")
    parser.add_argument("--model", default="BAAI/bge-m3", help="The sentence-transformer model to use.")
    parser.add_argument("--batch_size", type=int, default=16, help="Initial batch size for GPU processing.")
    args = parser.parse_args()
    
    generator = EmbeddingGenerator(args.db_name, args.model, args.batch_size)
    generator.run()

if __name__ == "__main__":
    main()
