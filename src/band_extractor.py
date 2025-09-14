#!/usr/bin/env python3
"""
Band Extractor - Extract distinct color bands from stepped gradient images
"""

import argparse
from PIL import Image
import numpy as np
from collections import Counter
from typing import List, Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def extract_bands_from_image(image_path: str, output_file: str = None, min_band_height: int = 10) -> List[Tuple[int, int, int]]:
    """
    Extract distinct color bands from a stepped gradient image.
    
    Args:
        image_path: Path to the input image
        output_file: Optional output file for the band palette
        min_band_height: Minimum height for a band to be considered distinct
    
    Returns:
        List of RGB color tuples representing each band
    """
    # Load image
    img = Image.open(image_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convert to numpy array
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Sample colors from the middle column to avoid edge effects
    middle_x = width // 2
    middle_column = img_array[:, middle_x]
    
    # Find distinct bands by analyzing color changes
    bands = []
    current_color = tuple(middle_column[0])
    band_start = 0
    
    for y in range(1, height):
        pixel_color = tuple(middle_column[y])
        
        # Calculate color difference
        color_diff = sum(abs(a - b) for a, b in zip(current_color, pixel_color))
        
        # If color change is significant, we have a new band
        if color_diff > 15:  # Threshold for color change
            # Calculate average color for this band
            band_height = y - band_start
            if band_height >= min_band_height:
                # Sample multiple pixels from the band for better accuracy
                band_pixels = middle_column[band_start:y]
                avg_color = tuple(np.mean(band_pixels, axis=0).astype(int))
                bands.append(avg_color)
            
            # Start new band
            current_color = pixel_color
            band_start = y
    
    # Add the last band
    if band_start < height:
        band_height = height - band_start
        if band_height >= min_band_height:
            band_pixels = middle_column[band_start:height]
            avg_color = tuple(np.mean(band_pixels, axis=0).astype(int))
            bands.append(avg_color)
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in bands:
                f.write(f"{rgb_to_hex(color)}\n")
        print(f"Extracted {len(bands)} distinct bands and saved to {output_file}")
    
    return bands

def extract_bands_with_analysis(image_path: str, output_file: str = None) -> List[Tuple[int, int, int]]:
    """
    Extract bands with detailed analysis of the image structure.
    """
    # Load image
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Sample from multiple columns for better accuracy
    sample_columns = [width // 4, width // 2, 3 * width // 4]
    all_bands = []
    
    for col in sample_columns:
        column = img_array[:, col]
        bands = []
        current_color = tuple(column[0])
        band_start = 0
        
        for y in range(1, height):
            pixel_color = tuple(column[y])
            color_diff = sum(abs(a - b) for a, b in zip(current_color, pixel_color))
            
            if color_diff > 20:  # Higher threshold for cleaner bands
                band_height = y - band_start
                if band_height >= 5:  # Minimum band height
                    # Get average color from the middle of the band
                    middle_y = band_start + band_height // 2
                    bands.append(tuple(column[middle_y]))
                
                current_color = pixel_color
                band_start = y
        
        # Add last band
        if band_start < height:
            middle_y = band_start + (height - band_start) // 2
            bands.append(tuple(column[middle_y]))
        
        all_bands.append(bands)
    
    # Find consensus bands (colors that appear in multiple columns)
    consensus_bands = []
    for i, bands in enumerate(all_bands):
        for band in bands:
            # Check if this color is similar to any existing consensus band
            is_new = True
            for existing in consensus_bands:
                diff = sum(abs(a - b) for a, b in zip(band, existing))
                if diff < 30:  # Similar color
                    is_new = False
                    break
            
            if is_new:
                consensus_bands.append(band)
    
    # Sort bands by luminance (brightness)
    def luminance(rgb):
        return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    
    consensus_bands.sort(key=luminance)
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in consensus_bands:
                f.write(f"{rgb_to_hex(color)}\n")
        print(f"Extracted {len(consensus_bands)} distinct bands and saved to {output_file}")
    
    return consensus_bands

def main():
    parser = argparse.ArgumentParser(description='Extract distinct color bands from gradient images')
    parser.add_argument('--image', required=True, help='Input image file')
    parser.add_argument('--output', help='Output palette file')
    parser.add_argument('--method', choices=['simple', 'analysis'], default='analysis',
                       help='Extraction method')
    parser.add_argument('--min-height', type=int, default=10, help='Minimum band height')
    
    args = parser.parse_args()
    
    if args.method == 'simple':
        bands = extract_bands_from_image(args.image, args.output, args.min_height)
    else:
        bands = extract_bands_with_analysis(args.image, args.output)
    
    print(f"Found {len(bands)} distinct color bands:")
    for i, color in enumerate(bands):
        print(f"Band {i+1}: {rgb_to_hex(color)} {color}")

if __name__ == '__main__':
    main()
