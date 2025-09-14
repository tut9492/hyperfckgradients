#!/usr/bin/env python3
"""
Balanced Color Extractor - Prioritizes darker tones and creates more balanced palettes.
"""

import argparse
from PIL import Image
import numpy as np
from collections import Counter

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def calculate_luminance(rgb):
    """Calculate luminance of an RGB color."""
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def extract_balanced_colors(image_path, num_colors=50, dark_bias=0.7, output_file=None):
    """
    Extract colors with bias toward darker tones.
    
    Args:
        image_path: Path to the input image
        num_colors: Number of colors to extract
        dark_bias: Bias toward darker colors (0.0 = no bias, 1.0 = only dark)
        output_file: Optional output file for the color palette
    """
    # Load image
    img = Image.open(image_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize image for faster processing
    img = img.resize((300, 300))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Reshape to list of pixels
    pixels = img_array.reshape(-1, 3)
    
    # Count color frequencies
    color_counts = Counter(map(tuple, pixels))
    
    # Get more colors than needed for better selection
    all_colors = color_counts.most_common(num_colors * 3)
    
    # Separate colors by luminance ranges
    dark_colors = []      # luminance 0-85
    mid_colors = []       # luminance 85-170  
    light_colors = []     # luminance 170-255
    
    for color, count in all_colors:
        luminance = calculate_luminance(color)
        if luminance <= 85:
            dark_colors.append((color, count, luminance))
        elif luminance <= 170:
            mid_colors.append((color, count, luminance))
        else:
            light_colors.append((color, count, luminance))
    
    # Calculate how many colors to take from each range
    if dark_bias > 0.5:
        # More dark colors
        dark_count = int(num_colors * dark_bias)
        mid_count = int(num_colors * (1 - dark_bias) * 0.6)
        light_count = num_colors - dark_count - mid_count
    else:
        # Balanced distribution
        dark_count = int(num_colors * 0.4)
        mid_count = int(num_colors * 0.4)
        light_count = num_colors - dark_count - mid_count
    
    # Select colors from each range
    selected_colors = []
    
    # Sort by frequency and take top colors from each range
    dark_colors.sort(key=lambda x: x[1], reverse=True)
    mid_colors.sort(key=lambda x: x[1], reverse=True)
    light_colors.sort(key=lambda x: x[1], reverse=True)
    
    selected_colors.extend([color for color, count, lum in dark_colors[:dark_count]])
    selected_colors.extend([color for color, count, lum in mid_colors[:mid_count]])
    selected_colors.extend([color for color, count, lum in light_colors[:light_count]])
    
    # Convert to hex and sort by luminance
    hex_colors = [rgb_to_hex(color) for color in selected_colors]
    hex_colors.sort(key=lambda x: calculate_luminance(hex_to_rgb(x)))
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in hex_colors:
                f.write(f"{color}\n")
        print(f"Extracted {len(hex_colors)} balanced colors and saved to {output_file}")
        print(f"Dark bias: {dark_bias}, Distribution: {dark_count} dark, {mid_count} mid, {light_count} light")
    
    return hex_colors

def create_dark_heavy_palette(image_path, num_colors=50, output_file=None):
    """
    Create a palette heavily weighted toward darker tones.
    """
    return extract_balanced_colors(image_path, num_colors, dark_bias=0.8, output_file=output_file)

def main():
    parser = argparse.ArgumentParser(description='Extract balanced colors from an image')
    parser.add_argument('--image', required=True, help='Input image file')
    parser.add_argument('--num-colors', type=int, default=50, help='Number of colors to extract')
    parser.add_argument('--dark-bias', type=float, default=0.7, help='Bias toward darker colors (0.0-1.0)')
    parser.add_argument('--output', help='Output palette file')
    parser.add_argument('--mode', choices=['balanced', 'dark-heavy'], default='balanced', 
                       help='Extraction mode')
    
    args = parser.parse_args()
    
    if args.mode == 'dark-heavy':
        colors = create_dark_heavy_palette(args.image, args.num_colors, args.output)
    else:
        colors = extract_balanced_colors(args.image, args.num_colors, args.dark_bias, args.output)
    
    print(f"Extracted {len(colors)} colors from {args.image}")
    
    if not args.output:
        print("Colors found:")
        for color in colors:
            print(color)

if __name__ == '__main__':
    main()


