import time
import multiprocessing
from . import utils

def run_multiprocessing(image_paths, output_dir, num_processes=None, prefix="mp"):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
        
    print(f"Starting Multiprocessing with {num_processes} processes for {len(image_paths)} images...")
    start_time = time.time()
    
    tasks = [(path, output_dir, f"{prefix}_{num_processes}") for path in image_paths]
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(utils.process_single_image, tasks)
        
    end_time = time.time()
    print(f"Multiprocessing completed in {end_time - start_time:.4f} seconds.")
    return end_time - start_time
