import time
import os
import concurrent.futures
from . import utils

# Run image processing using concurrent.futures.ThreadPoolExecutor
def run_futures(image_paths, output_dir, max_workers=None, prefix="fut"):

    if max_workers is None:
        max_workers = os.cpu_count()
        
    print(f"Starting Concurrent.futures (ThreadPool) with {max_workers} workers for {len(image_paths)} images...")
    start_time = time.time()
    
    tasks = [(path, output_dir, f"{prefix}_{max_workers}") for path in image_paths]
    
    # Use ThreadPoolExecutor to manage a pool of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(utils.process_single_image, tasks)
        
    end_time = time.time()
    print(f"Concurrent.futures completed in {end_time - start_time:.4f} seconds.")
    return end_time - start_time
