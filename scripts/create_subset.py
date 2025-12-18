import os
import shutil
import random

# Create a subset of the dataset by copying 10 images from each class folder
def create_subset(source_root, dest_root, images_per_class=5):
    """
    Creates a subset of the dataset by copying 'images_per_class' from each class folder.
    """
    images_dir = os.path.join(source_root, 'food-101', 'images')
    
    if not os.path.exists(images_dir):
        print(f"Error: Source images directory not found at {images_dir}")
        return

    if not os.path.exists(dest_root):
        os.makedirs(dest_root)
        
    classes = [d for d in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, d))]
    print(f"Found {len(classes)} classes.")
    
    total_copied = 0
    
    for cls in classes:
        src_class_dir = os.path.join(images_dir, cls)
        
        images = [f for f in os.listdir(src_class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # Retrieve the first N images from each class folder
        selected = images[:images_per_class]
        
        for img_name in selected:
            src_path = os.path.join(src_class_dir, img_name)
            new_name = f"{cls}_{img_name}"
            dst_path = os.path.join(dest_root, new_name)
            shutil.copy2(src_path, dst_path)
            total_copied += 1
            
    print(f"Successfully created subset with {total_copied} images in {dest_root}")

if __name__ == "__main__":
    source = "data"
    dest = "data/raw"
    count = 10
    
    if os.path.exists(dest):
        print(f"Clearing {dest}...")
        shutil.rmtree(dest)
    os.makedirs(dest)
    
    create_subset(source, dest, images_per_class=count)