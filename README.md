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

Note: The Food-101 dataset is not included in the GitHub repository due to its size.

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
This result is entirely reasonable and does not indicate super-linear speedup. Since the number of workers is less than the available vCPUs, no hardware oversubscription occurs. The observed speedup being lower than the ideal linear speedup of 16 is expected and healthy. It reflects unavoidable overheads, including sequential sections of the program, inter-process communication costs, and operating system scheduling overhead. 

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

## Scalability Analysis
Scalability is assessed by the reduction in execution time as worker count increases on the GCP instance. The multiprocessing implementation exhibits strong scalability, with speedup increasing from 1.99× at 2 workers to 13.15× at 16 workers, while maintaining high efficiency. In contrast, the concurrent.futures implementation shows limited scalability, achieving reasonable performance only up to 4 workers before efficiency drops sharply to 44% at 8 workers and 18% at 16 workers. This difference arises from architectural design: multiprocessing uses process-based parallelism that bypasses Python’s Global Interpreter Lock (GIL), enabling near-linear scaling, whereas concurrent.futures relies on thread-based parallelism that is increasingly constrained by GIL contention at higher worker counts.

## Bottlenecks
The primary bottleneck for both implementations is the serial fraction, including disk I/O and image decoding/encoding, which limits achievable speedup as predicted by Amdahl’s Law. For multiprocessing, efficiency decreases from 95.0% at 8 workers to 82.2% at 16 workers, indicating diminishing returns as I/O and coordination overheads dominate. A secondary bottleneck is hardware saturation: scaling beyond the available 8 CPU cores introduces context switching, inter-process communication, and memory contention, reducing efficiency. In the concurrent.futures implementation, bottlenecks are dominated by GIL contention, where increased thread counts lead to scheduling overhead and reduced parallel effectiveness, causing performance degradation at higher worker counts.

## Why Experimental Speedup Exceeds Theoretical Amdahl Speedup
The experimental speedup observed on Google Cloud Platform is higher than that obtained from local execution and exceeds the theoretical speedup predicted by Amdahl’s Law (approximately 6.40×). The GCP virtual machine provides a significantly larger number of available vCPUs, reduced resource contention, and a more stable runtime environment compared to a typical local system. As a result, worker processes can execute truly in parallel without oversubscription which leads to higher effective CPU utilization.

Theoretical models such as Amdahl’s Law rely on simplified assumptions and conservative estimates of the sequential fraction, and they do not account for hardware-level optimizations, caching effects, or runtime behavior. Consequently, real-world experimental performance may exceed theoretical predictions without violating parallel computing principles.












