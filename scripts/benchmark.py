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
from src import metrics

def load_config(config_path="config.yaml"):
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}. Using defaults.")
        return {"input_path": "data", "output_path": "data/processed"}

def run_benchmark():
    config = load_config()
    input_dir = config.get("input_path", "data")
    output_dir = config.get("output_path", "data/processed")

    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} not found.")
        return

    images = utils.get_image_files(input_dir)
    num_images = len(images)
    print(f"Running benchmark with {num_images} images from {input_dir}...")

    print(f"Using Amdahl's Law with Sequential Fraction (f) = {metrics.SEQUENTIAL_FRACTION}")

    # Helper to print intermediate tables
    def print_mode_table(title, subset_results):
        print(f"\nResults for {title}")
        print(f"{'Workers':<10} | {'Time (s)':<10} | {'Speedup':<10} | {'Efficiency':<10}")
        print("-" * 55)
        
        for _, workers, duration in subset_results:
            speedup = metrics.calculate_amdahl_speedup(workers)
            efficiency = metrics.calculate_efficiency(speedup, workers)
            
            print(f"{workers:<10} | {duration:<10.4f} | {speedup:<10.2f} | {efficiency:<10.2f}")

    if os.path.exists(output_dir):
        for i in range(3):
            try:
                shutil.rmtree(output_dir)
                break
            except OSError as e:
                print(f"Cleanup attempt {i+1} failed: {e}. Retrying...")
                time.sleep(1)
                
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    # 1. Sequential
    sequential_results = []
    print("\n--- Running Sequential ---")
    duration = sequential.run_sequential(images, output_dir, prefix="sequential")
    entry = ("Sequential", 1, duration)
    results.append(entry)
    sequential_results.append(entry)
    
    print_mode_table("Sequential", sequential_results)
    
    # 2. Multiprocessing
    mp_results = []
    for workers in [2, 4, 8, 16]:
        print(f"\n--- Running Multiprocessing (Workers={workers}) ---")
        duration = multiprocessing_module.run_multiprocessing(images, output_dir, workers, prefix="mp")
        entry = ("Multiprocessing", workers, duration)
        results.append(entry)
        mp_results.append(entry)
        
    print_mode_table("Multiprocessing", mp_results)
        
    # 3. Futures
    futures_results = []
    for workers in [2, 4, 8, 16]:
        print(f"\n--- Running Futures (Workers={workers}) ---")
        duration = concurrent_futures_module.run_futures(images, output_dir, workers, prefix="futures")
        entry = ("Futures", workers, duration)
        results.append(entry)
        futures_results.append(entry)
        
    print_mode_table("Futures", futures_results)
        
    # Final Analysis
    print("FINAL SUMMARY")
    print(f"{'Mode':<20} | {'Workers':<10} | {'Time (s)':<10} | {'Speedup':<10} | {'Efficiency':<10}")
    print("-" * 75)
    
    for mode, workers, duration in results:
        speedup = metrics.calculate_amdahl_speedup(workers)
        efficiency = metrics.calculate_efficiency(speedup, workers)
            
        speedup_str = f"{speedup:.2f}x"
        efficiency_str = f"{efficiency:.2f}"
        print(f"{mode:<20} | {workers:<10} | {duration:<10.4f} | {speedup_str:<10} | {efficiency_str:<10}")
    print("="*75)

if __name__ == "__main__":
    run_benchmark()
