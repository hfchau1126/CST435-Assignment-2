import time
from . import utils

def run_sequential(image_paths, output_dir, prefix="seq"):
    print(f"Starting Sequential processing of {len(image_paths)} images...")
    start_time = time.time()
    
    for path in image_paths:
        utils.process_single_image((path, output_dir, prefix))
        
    end_time = time.time()
    print(f"Sequential processing completed in {end_time - start_time:.4f} seconds.")
    return end_time - start_time
