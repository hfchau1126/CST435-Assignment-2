import os
import shutil
import random

# Create a subset of the dataset by copying 10 images from each class folder
def create_subset(source_root, dest_root, images_per_class=None, total_images=None):
 
    images_dir = os.path.join(source_root, 'food-101', 'images')
    
    if not os.path.exists(images_dir):
        print(f"Error: Source images directory not found at {images_dir}")
        return

    if not os.path.exists(dest_root):
        os.makedirs(dest_root)
        
    classes = [d for d in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, d))]
    num_classes = len(classes)
    print(f"Found {num_classes} classes.")
    
    base_count = 0
    remainder = 0
    
    # Calculate how many images to take from each class
    if total_images is not None and num_classes > 0:
        base_count = total_images // num_classes
        remainder = total_images % num_classes
        print(f"Targeting {total_images} images: {base_count} per class, plus {remainder} extra distributed.")
    elif images_per_class is not None:
        base_count = images_per_class
    else:
        base_count = 10 
    
    total_copied = 0
    
    for i, cls in enumerate(classes):
        current_limit = base_count
        # Distribute the extra images among the first few classes
        if i < remainder:
            current_limit += 1
            
        src_class_dir = os.path.join(images_dir, cls)
        
        images = [f for f in os.listdir(src_class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # Retrieve the first N images from each class folder
        selected = images[:current_limit]
        
        for img_name in selected:
            src_path = os.path.join(src_class_dir, img_name)
            # Prefix filename with class name to avoid collision and preserve label info
            new_name = f"{cls}_{img_name}"
            dst_path = os.path.join(dest_root, new_name)
            shutil.copy2(src_path, dst_path)
            total_copied += 1
            
    print(f"Successfully created subset with {total_copied} images in {dest_root}")

if __name__ == "__main__":
    source = "C:/Users/waipe/OneDrive/Desktop"
    dest = "data/raw"
    target_total = 1000
    
    if os.path.exists(dest):
         print(f"Clearing {dest}...")
         shutil.rmtree(dest)
    os.makedirs(dest)
    create_subset(source, dest, total_images=target_total)
