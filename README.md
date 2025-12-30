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
  - food-101 (dataset)
  - processed (empty before run)
  - raw (empty before run)
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

The benchmark calculates **Theoretical Speedup** and **Efficiency** using **Amdahl's Law** with a fixed sequential fraction ($f=0.05$).

**Formulas:**
- **Speedup**: $S = \frac{1}{f + \frac{1-f}{P}}$
- **Efficiency**: $E = \frac{S}{P}$

Where:
- $f = 0.05$ (Sequential Fraction)
- $P$ = Number of Workers


