#!/usr/bin/env python3
"""
Sensitive Band Extractor - Extract all visible color bands from gradient images
"""

import argparse
from PIL import Image
import numpy as np
from typing import List, Tuple

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def extract_all_bands(image_path: str, output_file: str = None, sensitivity: int = 5) -> List[Tuple[int, int, int]]:
    """
    Extract ALL visible color bands with high sensitivity.
    
    Args:
        image_path: Path to the input image
        output_file: Optional output file for the band palette
        sensitivity: Color change sensitivity (lower = more sensitive)
    
    Returns:
        List of RGB color tuples representing each band
    """
    # Load image
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Sample from the middle column
    middle_x = width // 2
    middle_column = img_array[:, middle_x]
    
    bands = []
    current_color = tuple(middle_column[0])
    band_start = 0
    
    print(f"Analyzing {height} pixels with sensitivity {sensitivity}")
    
    for y in range(1, height):
        pixel_color = tuple(middle_column[y])
        
        # Calculate color difference (much more sensitive)
        color_diff = sum(abs(int(a) - int(b)) for a, b in zip(current_color, pixel_color))
        
        # If color change is detected, we have a new band
        if color_diff > sensitivity:
            # Get the color from the middle of this band
            band_height = y - band_start
            if band_height >= 1:  # Accept even single-pixel bands
                middle_y = band_start + band_height // 2
                band_color = tuple(middle_column[middle_y])
                bands.append(band_color)
                print(f"Band {len(bands)}: {rgb_to_hex(band_color)} at y={middle_y}")
            
            # Start new band
            current_color = pixel_color
            band_start = y
    
    # Add the last band
    if band_start < height:
        middle_y = band_start + (height - band_start) // 2
        band_color = tuple(middle_column[middle_y])
        bands.append(band_color)
        print(f"Band {len(bands)}: {rgb_to_hex(band_color)} at y={middle_y}")
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in bands:
                f.write(f"{rgb_to_hex(color)}\n")
        print(f"\nExtracted {len(bands)} distinct bands and saved to {output_file}")
    
    return bands

def extract_bands_with_sampling(image_path: str, output_file: str = None) -> List[Tuple[int, int, int]]:
    """
    Extract bands by sampling every few pixels and finding unique colors.
    """
    # Load image
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Sample every 5 pixels from the middle column
    middle_x = width // 2
    sampled_colors = []
    
    for y in range(0, height, 5):  # Sample every 5 pixels
        color = tuple(img_array[y, middle_x])
        sampled_colors.append(color)
    
    # Find unique colors (with some tolerance)
    unique_colors = []
    tolerance = 10  # Color difference tolerance
    
    for color in sampled_colors:
        is_unique = True
        for existing in unique_colors:
            diff = sum(abs(int(a) - int(b)) for a, b in zip(color, existing))
            if diff < tolerance:
                is_unique = False
                break
        
        if is_unique:
            unique_colors.append(color)
    
    # Sort by position in image (top to bottom)
    def get_color_position(color):
        for i, sampled_color in enumerate(sampled_colors):
            if sampled_color == color:
                return i
        return 0
    
    unique_colors.sort(key=get_color_position)
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in unique_colors:
                f.write(f"{rgb_to_hex(color)}\n")
        print(f"Extracted {len(unique_colors)} unique colors and saved to {output_file}")
    
    return unique_colors

def main():
    parser = argparse.ArgumentParser(description='Extract all visible color bands from gradient images')
    parser.add_argument('--image', required=True, help='Input image file')
    parser.add_argument('--output', help='Output palette file')
    parser.add_argument('--method', choices=['sensitive', 'sampling'], default='sensitive',
                       help='Extraction method')
    parser.add_argument('--sensitivity', type=int, default=5, help='Color change sensitivity')
    
    args = parser.parse_args()
    
    if args.method == 'sensitive':
        bands = extract_all_bands(args.image, args.output, args.sensitivity)
    else:
        bands = extract_bands_with_sampling(args.image, args.output)
    
    print(f"\nTotal bands found: {len(bands)}")

if __name__ == '__main__':
    main()
