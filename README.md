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

## Key Features

- **Accumulated Output**: Processed images from all benchmark runs (Sequential, Multiprocessing, Futures) are saved with unique prefixes (e.g., `processed_mp_4_image.jpg`) to the `data/processed` directory.
- **Intermediate Results**: Performance tables are printed after each mode completes, providing real-time feedback.
- **Robust Cleanup**: Includes retry logic for directory cleanup to handle Windows file locking.

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
| Paradigm | Workers | Time (s) | Speedup | Efficiency | P Value | 
|----------|---------|----------|---------|------------|---------|
| Sequential | 1 | 30.1993 | 1.00 | 100.0% | 1.0000 | 
| Multiprocessing | 2 | 15.2065 | 1.99 | 99.5% | 0.9929 | 
| Multiprocessing | 4 | 7.6327 | 3.96 | 99.0% | 0.9963 | 
| Multiprocessing | 8 | 3.9748 | 7.60 | 95.0% | 0.9924 | 
| Multiprocessing | 16 | 2.2967 | 13.15 | 82.2% | 0.9855 |
| Futures | 2 | 14.9852 | 2.02 | 101.0% | 1.0076* | 
| Futures | 4 | 9.4734 | 3.19 | 79.8% | 0.9151 | 
| Futures | 8 | 8.5799 | 3.52 | 44.0% | 0.8182 | 
| Futures | 16 | 10.2706 | 2.94 | 18.4% | 0.7039 |

## Explanation of Results

### Multiprocessing Results

The multiprocessing implementation shows strong and consistent scalability:

Speedup increases steadily as the number of workers increases

At 16 workers, a speedup of approximately 13× is achieved

Efficiency remains high (above 80%) at larger worker counts

### Concurrent.futures Results

