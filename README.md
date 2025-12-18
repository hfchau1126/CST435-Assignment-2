# Parallel Image Processing System (Python)

This project implements a parallel image processing pipeline that applies a sequence of filters (Grayscale, Gaussian Blur, Sobel Edge Detection, Sharpening, Brightness) to a collection of images.

## Project Structure

- `src/`: Source code
  - `image_processing.py`: Implementation of image filters
  - `sequential.py`: Logic for sequential execution
  - `multiprocessing_module.py`: Logic for multiprocessing execution
  - `concurrent_futures_module.py`: Logic for concurrent futures execution
  - `utils.py`: Helper functions for I/O
- `scripts/`: Executable scripts
  - `benchmark.py`: Runs performance comparison
  - `create_subset.py`: Helper to create dataset subset
- `data/`: Directory for input (raw) and output (processed) images
  - food-101
  - processed
  - raw
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

