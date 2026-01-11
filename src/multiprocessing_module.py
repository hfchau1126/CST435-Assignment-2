import time
import multiprocessing
from . import utils

# Run image processing using multiple processes
def run_multiprocessing(image_paths, output_dir, num_processes=None, prefix="mp"):

    # If no number of processes is specified, default to the number of CPU cores available
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
        
    print(f"Starting Multiprocessing with {num_processes} processes for {len(image_paths)} images...")
    start_time = time.time()
    
    # Prepare arguments for each task (image) to be passed to the worker function
    tasks = [(path, output_dir, f"{prefix}_{num_processes}") for path in image_paths]
    
    # Initialize a Pool of worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Map the 'process_single_image' function to the list of tasks
        pool.map(utils.process_single_image, tasks)
        
    end_time = time.time()
    print(f"Multiprocessing completed in {end_time - start_time:.4f} seconds.")
    return end_time - start_time
