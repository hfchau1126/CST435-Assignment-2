import numpy as np
from PIL import Image

# Convert RGB image to grayscale
def to_grayscale(image_array):
    if len(image_array.shape) == 2:
        return image_array 
    
    r, g, b = image_array[:,:,0], image_array[:,:,1], image_array[:,:,2]
    grayscale = 0.299 * r + 0.587 * g + 0.114 * b
    return grayscale.astype(np.uint8)

# Apply 3x3 Gaussian Blur
def gaussian_blur(image_array):
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16.0
    return apply_convolution(image_array, kernel)

# Apply Sobel Edge Detection.
def sobel_edge_detection(image_array):
    # Convert to grayscale first if needed
    if len(image_array.shape) == 3:
        gray = to_grayscale(image_array)
    else:
        gray = image_array
        
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    
    Ix = apply_convolution_2d(gray, Kx)
    Iy = apply_convolution_2d(gray, Ky)
    
    magnitude = np.hypot(Ix, Iy)
    magnitude = magnitude / magnitude.max() * 255
    return magnitude.astype(np.uint8)

# Sharpen image using a kernel.
def sharpen(image_array):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return apply_convolution(image_array, kernel)

# Adjust brightness by a factor
def adjust_brightness(image_array, factor=1.2):
    adjusted = image_array * factor
    adjusted = np.clip(adjusted, 0, 255)
    return adjusted.astype(np.uint8)

# Apply convolution to an image 
def apply_convolution(image_array, kernel):
    if len(image_array.shape) == 3:
        # RGB
        r = apply_convolution_2d(image_array[:,:,0], kernel)
        g = apply_convolution_2d(image_array[:,:,1], kernel)
        b = apply_convolution_2d(image_array[:,:,2], kernel)
        return np.dstack((r, g, b)).astype(np.uint8)
    else:
        # Grayscale
        return apply_convolution_2d(image_array, kernel).astype(np.uint8)

# Simple 2D convolution implementation
def apply_convolution_2d(image_2d, kernel):
    pad_height = kernel.shape[0] // 2
    pad_width = kernel.shape[1] // 2
    
    padded = np.pad(image_2d, ((pad_height, pad_height), (pad_width, pad_width)), mode='edge')
    
    # Kernel assumed 3x3 for simplicity
    if kernel.shape == (3, 3):
        p = padded.astype(float)
        
        # Slices
        top_left = p[:-2, :-2]
        top_mid = p[:-2, 1:-1]
        top_right = p[:-2, 2:]
        
        mid_left = p[1:-1, :-2]
        center = p[1:-1, 1:-1]
        mid_right = p[1:-1, 2:]
        
        bot_left = p[2:, :-2]
        bot_mid = p[2:, 1:-1]
        bot_right = p[2:, 2:]
        
        output = (
            top_left * kernel[0,0] + top_mid * kernel[0,1] + top_right * kernel[0,2] +
            mid_left * kernel[1,0] + center * kernel[1,1] + mid_right * kernel[1,2] +
            bot_left * kernel[2,0] + bot_mid * kernel[2,1] + bot_right * kernel[2,2]
        )
        
        return np.clip(output, 0, 255).astype(np.uint8)
    else:
        raise NotImplementedError("Only 3x3 kernel supported for this optimization.")

def apply_filters(image_array):
    if image_array is None:
        return None
        
    # Step 1: Grayscale
    gray = to_grayscale(image_array)
    
    # Step 2: Blur (on grayscale)
    blurred = gaussian_blur(gray)
    
    # Step 3: Edge Detection
    edges = sobel_edge_detection(blurred)
    
    # Step 4: Sharpen (Enhance the edges)
    sharpened = sharpen(edges)
    
    # Step 5: Brightness
    bright = adjust_brightness(sharpened, factor=1.2)
    
    return bright