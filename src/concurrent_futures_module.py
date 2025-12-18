import time
import os
import concurrent.futures
from . import utils

def run_futures(image_paths, output_dir, max_workers=None):
    if max_workers is None:
        max_workers = os.cpu_count()
        
    print(f"Starting Concurrent.futures (ProcessPool) with {max_workers} workers for {len(image_paths)} images...")
    start_time = time.time()
    
    tasks = [(path, output_dir) for path in image_paths]
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(utils.process_single_image, tasks)
        
    end_time = time.time()
    print(f"Concurrent.futures completed in {end_time - start_time:.4f} seconds.")
    return end_time - start_time