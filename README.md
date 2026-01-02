# Parallel Image Processing System (Python)

This project implements a parallel image processing pipeline that applies a sequence of filters (Grayscale, Gaussian Blur, Sobel Edge Detection, Sharpening, Brightness) to a collection of images.

## Project Structure

- `src/`: Source code
  - `image_processing.py`: Implementation of image filters
  - `sequential.py`: Logic for sequential execution
  - `multiprocessing_module.py`: Logic for multiprocessing execution
  - `concurrent_futures_module.py`: Logic for concurrent futures execution
  - `metrics.py`: calculations for Speedup and Efficiency
  - `utils.py`: Helper functions for I/O
- `scripts/`: Executable scripts
  - `benchmark.py`: Runs performance comparison
  - `create_subset.py`: Helper to create dataset subset
- `data/`: Directory for input (raw) and output (processed) images
- `config.yaml`: Configuration settings
- `requirements.txt`: Python dependencies

## Setup

Requires Python 3.x. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running Benchmarks

To process the images in `data/raw` and compare performance:

```bash
python scripts/benchmark.py
```

Outputs will be saved to `data/processed`.

## Performance Metrics

The benchmark calculates both **Actual Speedup** and **Theoretical Speedup** to analyze performance.

**Metrics:**
- **Actual Speedup ($S_{actual}$)**: $S_{actual} = \frac{T(1)}{T(N)}$
  
- **Theoretical Speedup ($S_{theo}$)**: Uses **Amdahl's Law** with a fixed sequential fraction ($f=0.1$).
  - $S_{theo} = \frac{1}{f + \frac{1-f}{P}}$
    
- **Efficiency ($E$)**: $E = \frac{S_{actual}}{P}$
  
- **Estimated Parallel Fraction ($P_{frac}$)**: Derived from the actual speedup to estimate the parallelizable portion of the code.
  - $P_{frac} = \frac{\frac{1}{S_{actual}} - 1}{\frac{1}{N} - 1}$

Where:
- $T(1)$ = Time taken by Sequential execution
- $T(N)$ = Time taken by $P$ workers
- $P$ = Number of Workers

## Results Summary
| Paradigm | Workers | Time (s) | Actual Speedup | Theoretical Speedup | Efficiency | P Value | 
|----------|---------|----------|---------|------------|---------|---------|
| Sequential | 1 | 30.1993 | 1.00x | 1.00x | 100.0% | 1.0000 |
| Multiprocessing | 2 | 15.2065 | 1.99x | 1.82x | 99.5%  | 0.9929 | 
| Multiprocessing | 4 | 7.6327 | 3.96x | 3.08x | 99.0%  | 0.9963 | 
| Multiprocessing | 8 | 3.9748 | 7.60x | 4.71x | 95.0% | 0.9924 |
| Multiprocessing | 16 | 2.2967 | 13.15x | 6.40x | 82.2% | 0.9855 |
| Futures | 2 | 14.9852 | 2.02x | 1.82x | 101.0% | 1.0076* |
| Futures | 4 | 9.4734 | 3.19x | 3.08x | 79.8% | 0.9151 |
| Futures | 8 | 8.5799 | 3.52x | 4.71x | 44.0% | 0.8182 |
| Futures | 16 | 10.2706 | 2.94x | 6.40x | 18.4% | 0.7039 |

## Explanation of Results

### Multiprocessing Results

- Speedup increases steadily as the number of workers increases.
- At 16 workers, a speedup of approximately 13× is achieved.
- Efficiency remains high (above 80%) at larger worker counts.

**Summary:** 
This result is entirely reasonable and does not indicate super-linear speedup. Since the number of workers is less than the available vCPUs, no hardware oversubscription occurs.The observed speedup being lower than the ideal linear speedup of 16 is expected and healthy. It reflects unavoidable overheads, including sequential sections of the program, inter-process communication costs, and operating system scheduling overhead. 

### Concurrent.futures Results

- Speedup improves slightly at low thread counts.
- Performance saturates around 3–4× speedup.
- Execution time increases when using more than 8 threads.
- Efficiency drops sharply at higher thread counts.

ThreadPoolExecutor achieved significant speedup (up to 3.52x) despite Python's Global Interpreter Lock (GIL).

**Root Cause Investigation:**
1. **Image Processing Libraries**: OpenCV and NumPy release the GIL during C-level operations
2. **I/O-Bound Nature**: Image loading and saving dominates computation time
3. **GIL Bypass**: Heavy computation happens in C extensions, not Python bytecode

**Evidence:**
- Pure Python CPU-bound threads would show ~1.0x speedup
- Measured 2.02-3.52x speedup indicates GIL is not the bottleneck
- Performance degrades at 16 workers due to thread contention, not GIL

**Summary:** 
The image processing pipeline is sufficiently I/O-bound or uses enough C extensions that ThreadPoolExecutor provides meaningful parallelism despite Python's GIL.

## Why Experimental Speedup Exceeds Theoretical Amdahl Speedup
The theoretical speedup predicted by Amdahl’s Law for 16 workers is significantly lower (approximately 6.40×) than the experimentally observed speedup. It indicates that the estimated sequential fraction 𝑓 derived from the theoretical model is conservative.

Amdahl’s Law assumes uniform workload distribution, constant memory behavior, and no cache effects. In practice, the experimental system benefits from improved CPU cache locality, operating system file caching, and reduced per-process interpreter overhead when multiple processes execute concurrently. As a result, the theoretical model underestimates observed performance due to conservative assumptions of uniform workload and constant memory behavior.







