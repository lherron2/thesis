#!/usr/bin/env python3
"""Convert large PNG files to JPEG for better compression."""

import os
from PIL import Image

FIGURES_DIR = "/home/lukas/research/thesis/figures"
SRC_DIR = "/home/lukas/research/thesis/src"
MAX_DIMENSION = 1600  # Reduce further
JPEG_QUALITY = 80

def convert_png_to_jpg(filepath):
    """Convert PNG to JPEG."""
    try:
        img = Image.open(filepath)
        original_size = os.path.getsize(filepath)

        # Skip small files
        if original_size < 200000:  # < 200KB
            return 0

        width, height = img.size

        # Resize if too large
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            ratio = min(MAX_DIMENSION / width, MAX_DIMENSION / height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Convert to RGB (JPEG doesn't support alpha)
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Save as JPEG
        jpg_path = filepath.replace('.png', '.jpg')
        img.save(jpg_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)

        new_size = os.path.getsize(jpg_path)
        reduction = (1 - new_size / original_size) * 100

        print(f"{os.path.basename(filepath)}: {original_size/1024:.0f}KB -> {new_size/1024:.0f}KB ({reduction:.0f}%)")

        # Remove original PNG
        os.remove(filepath)

        return original_size - new_size
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return 0

def update_tex_references():
    """Update .tex files to use .jpg instead of .png."""
    for filename in os.listdir(SRC_DIR):
        if filename.endswith('.tex'):
            filepath = os.path.join(SRC_DIR, filename)
            with open(filepath, 'r') as f:
                content = f.read()

            # Replace .png with .jpg in includegraphics
            new_content = content.replace('.png}', '.jpg}')

            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated: {filename}")

def main():
    total_saved = 0
    files = [f for f in os.listdir(FIGURES_DIR) if f.endswith('.png')]

    print(f"Converting {len(files)} PNG files to JPEG...")

    for filename in sorted(files):
        filepath = os.path.join(FIGURES_DIR, filename)
        saved = convert_png_to_jpg(filepath)
        total_saved += saved

    print(f"\nTotal space saved: {total_saved/1024/1024:.1f} MB")

    print("\nUpdating TeX references...")
    update_tex_references()

if __name__ == "__main__":
    main()
