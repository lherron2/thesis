#!/usr/bin/env python3
"""Compress PNG images to reduce PDF size."""

import os
from PIL import Image

FIGURES_DIR = "/home/lukas/research/thesis/figures"
MAX_DIMENSION = 2000  # Max width or height in pixels
JPEG_QUALITY = 85

def compress_png(filepath):
    """Compress a PNG file by resizing if too large and optimizing."""
    try:
        img = Image.open(filepath)
        original_size = os.path.getsize(filepath)

        # Get dimensions
        width, height = img.size

        # Resize if too large
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            ratio = min(MAX_DIMENSION / width, MAX_DIMENSION / height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"  Resized: {width}x{height} -> {new_size[0]}x{new_size[1]}")

        # Convert RGBA to RGB if needed (for better compression)
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Save as optimized PNG
        img.save(filepath, 'PNG', optimize=True)

        new_size = os.path.getsize(filepath)
        reduction = (1 - new_size / original_size) * 100

        if reduction > 5:
            print(f"  {os.path.basename(filepath)}: {original_size/1024/1024:.1f}MB -> {new_size/1024/1024:.1f}MB ({reduction:.0f}% reduction)")

        return original_size - new_size
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return 0

def main():
    total_saved = 0
    files = [f for f in os.listdir(FIGURES_DIR) if f.endswith('.png')]

    print(f"Processing {len(files)} PNG files...")

    # Sort by size, process largest first
    files_with_size = [(f, os.path.getsize(os.path.join(FIGURES_DIR, f))) for f in files]
    files_with_size.sort(key=lambda x: -x[1])

    for filename, size in files_with_size:
        if size > 500000:  # Only process files > 500KB
            filepath = os.path.join(FIGURES_DIR, filename)
            saved = compress_png(filepath)
            total_saved += saved

    print(f"\nTotal space saved: {total_saved/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()
