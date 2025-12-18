import time
import os
import shutil
import sys
import yaml

# Add parent directory to path to allow importing src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import sequential
from src import multiprocessing_module
from src import concurrent_futures_module
from src import utils

def load_config(config_path="config.yaml"):
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}. Using defaults.")
        return {"input_path": "data/raw", "output_path": "data/processed"}

def run_benchmark():
    # Load config
    config = load_config()
    input_dir = config.get("input_path", "data/raw")
    output_dir = config.get("output_path", "data/processed")
    
    # Check if data exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} not found.")
        return

    images = utils.get_image_files(input_dir)
    num_images = len(images)
    print(f"Running benchmark with {num_images} images from {input_dir}...")
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    results = []
    
    # 1. Sequential
    print("\n--- Running Sequential ---")
    duration = sequential.run_sequential(images, output_dir)
    results.append(("Sequential", 1, duration))
    
    # 2. Multiprocessing
    for workers in [2, 4, 8]:
        print(f"\n--- Running Multiprocessing (Workers={workers}) ---")
        duration = multiprocessing_module.run_multiprocessing(images, output_dir, workers)
        results.append(("Multiprocessing", workers, duration))
        
    # 3. Futures
    for workers in [2, 4, 8]:
        print(f"\n--- Running Futures (Workers={workers}) ---")
        duration = concurrent_futures_module.run_futures(images, output_dir, workers)
        results.append(("Futures", workers, duration))
        
    # Performance Analysis
    print("\n" + "="*50)
    print(f"{'Mode':<20} | {'Workers':<10} | {'Time (s)':<10} | {'Speedup':<10}")
    print("-" * 50)
    
    base_time = results[0][2]
    
    for mode, workers, duration in results:
        speedup = base_time / duration if duration > 0 else 0
        print(f"{mode:<20} | {workers:<10} | {duration:<10.4f} | {speedup:<10.2f}x")
    print("="*50)

if __name__ == "__main__":
    run_benchmark()