#!/usr/bin/env python3
"""
Extract colors from a gradient image while preserving the top-to-bottom order.
"""

import argparse
from PIL import Image
import numpy as np

def extract_ordered_colors(image_path, num_colors):
    """Extract colors from a gradient image in top-to-bottom order."""
    # Load the image
    img = Image.open(image_path)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get image dimensions
    width, height = img.size
    
    # Calculate step size to get the desired number of colors
    step = width // num_colors
    
    colors = []
    
    # Sample colors from left to right (horizontal gradient)
    for i in range(num_colors):
        x = i * step + (step // 2)  # Sample from middle of each band
        if x >= width:
            x = width - 1
        
        # Sample from the middle of the image vertically
        y = height // 2
        pixel = img.getpixel((x, y))
        
        # Convert to hex
        hex_color = f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
        colors.append(hex_color)
    
    return colors

def main():
    parser = argparse.ArgumentParser(description='Extract colors from gradient in order')
    parser.add_argument('--image', required=True, help='Path to gradient image')
    parser.add_argument('--num-colors', type=int, required=True, help='Number of colors to extract')
    parser.add_argument('--output', required=True, help='Output palette file')
    
    args = parser.parse_args()
    
    # Extract colors in order
    colors = extract_ordered_colors(args.image, args.num_colors)
    
    # Save to file
    with open(args.output, 'w') as f:
        for color in colors:
            f.write(f"{color}\n")
    
    print(f"Extracted {len(colors)} colors in gradient order")
    print(f"Saved to {args.output}")

if __name__ == "__main__":
    main()
