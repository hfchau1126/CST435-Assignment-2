import os
import time
import numpy as np
from PIL import Image
from . import image_processing

# Load an image from path and return as numpy array
def load_image(path):

    try:
        with Image.open(path) as img:
            return np.array(img.convert('RGB')) 
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

# Save numpy array as image
def save_image(image_array, path):

    try:
        img = Image.fromarray(image_array)
        img.save(path)
    except Exception as e:
        print(f"Error saving {path}: {e}")

# Return list of image file paths in directory.
def get_image_files(directory):

    valid_exts = {'.jpg', '.jpeg', '.png', '.bmp'}
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if os.path.splitext(f)[1].lower() in valid_exts]

# Wrapper for processing a single image
def process_single_image(args):

    input_path, output_dir, prefix = args
    filename = os.path.basename(input_path)
    
    # Step 1: Load the image into memory
    img = load_image(input_path)
    if img is None:
        return
        
    # Step 2: Apply image processing filters
    try:
        result = image_processing.apply_filters(img)
        
        # Step 3: Save the processed result to the output directory
        output_path = os.path.join(output_dir, f"processed_{prefix}_{filename}")
        save_image(result, output_path)
    except Exception as e:
        print(f"Failed to process {filename}: {e}")
