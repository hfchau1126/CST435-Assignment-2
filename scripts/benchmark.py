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
    
    if not images:
        print(f"No images found in {input_dir}. Auto-generating subset...")
        try:
            import create_subset
            # Default to 1000 images if not specified
            create_subset.create_subset(source_root="data", dest_root=input_dir, total_images=1000)
            images = utils.get_image_files(input_dir)
            if not images:
                print("Error: create_subset failed to generate images.")
                return
        except ImportError:
            print("Error: Could not import create_subset script.")
            return
        except Exception as e:
            print(f"Error generating subset: {e}")
            return
            
    num_images = len(images)
    print(f"Running benchmark with {num_images} images from {input_dir}...")

    print(f"Using Amdahl's Law with Theoretical Sequential Fraction (f) = {metrics.THEORETICAL_SEQUENTIAL_FRACTION}")

    # Helper to print intermediate tables
    def print_mode_table(title, subset_results, t_seq):
 
        print(f"\nResults for {title}")
        header = f"{'Workers':<10} | {'Time (s)':<10} | {'Actual S':<10} | {'Theo S':<10} | {'Diff':<10} | {'Estimated P':<10} | {'Efficiency':<10}"
        print(header)
        print("-" * len(header))
        
        for _, workers, duration in subset_results:
            actual_speedup = metrics.calculate_actual_speedup(t_seq, duration)
            theo_speedup = metrics.calculate_theoretical_speedup(workers)
            diff = theo_speedup - actual_speedup
            p_val = metrics.calculate_parallel_fraction(actual_speedup, workers)
            efficiency = metrics.calculate_efficiency(actual_speedup, workers)
            
            print(f"{workers:<10} | {duration:<10.4f} | {actual_speedup:<10.2f} | {theo_speedup:<10.2f} | {diff:<10.2f} | {p_val:<10.4f} | {efficiency:<10.2f}")

    # Clean up previous output directory to ensure fair write performance
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
    t_sequential = duration
    entry = ("Sequential", 1, duration)
    results.append(entry)
    sequential_results.append(entry)
    
    print_mode_table("Sequential", sequential_results, t_sequential)
    
    # 2. Multiprocessing
    mp_results = []
    for workers in [2, 4, 8, 16]:
        print(f"\n--- Running Multiprocessing (Workers={workers}) ---")
        duration = multiprocessing_module.run_multiprocessing(images, output_dir, workers, prefix="mp")
        entry = ("Multiprocessing", workers, duration)
        results.append(entry)
        mp_results.append(entry)
        
    print_mode_table("Multiprocessing", mp_results, t_sequential)
        
    # 3. Futures
    futures_results = []
    for workers in [2, 4, 8, 16]:
        print(f"\n--- Running Futures (Workers={workers}) ---")
        duration = concurrent_futures_module.run_futures(images, output_dir, workers, prefix="futures")
        entry = ("Futures", workers, duration)
        results.append(entry)
        futures_results.append(entry)
        
    print_mode_table("Futures", futures_results, t_sequential)
        
    # Final Analysis
    print("FINAL SUMMARY")
    header = f"{'Mode':<20} | {'Workers':<10} | {'Time (s)':<10} | {'Actual S':<10} | {'Theo S':<10} | {'Diff':<10} | {'Estimated P':<10} | {'Efficiency':<10}"
    print(header)
    print("-" * len(header))
    
    for mode, workers, duration in results:
        actual_speedup = metrics.calculate_actual_speedup(t_sequential, duration)
        theo_speedup = metrics.calculate_theoretical_speedup(workers)
        diff = theo_speedup - actual_speedup
        p_val = metrics.calculate_parallel_fraction(actual_speedup, workers)
        efficiency = metrics.calculate_efficiency(actual_speedup, workers)
            
        print(f"{mode:<20} | {workers:<10} | {duration:<10.4f} | {actual_speedup:<10.2f} | {theo_speedup:<10.2f} | {diff:<10.2f} | {p_val:<10.4f} | {efficiency:<10.2f}")
    print("="*75)

if __name__ == "__main__":
    run_benchmark()
