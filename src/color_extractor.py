#!/usr/bin/env python3
"""
Extract colors from an image using PIL and basic color analysis.
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

def extract_colors_from_image(image_path, num_colors=50, output_file=None):
    """
    Extract the most prominent colors from an image.
    
    Args:
        image_path: Path to the input image
        num_colors: Number of colors to extract
        output_file: Optional output file for the color palette
    
    Returns:
        List of hex color strings
    """
    # Load image
    img = Image.open(image_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize image for faster processing
    img = img.resize((200, 200))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Reshape to list of pixels
    pixels = img_array.reshape(-1, 3)
    
    # Count color frequencies
    color_counts = Counter(map(tuple, pixels))
    
    # Get the most common colors
    most_common_colors = color_counts.most_common(num_colors)
    
    # Extract just the colors
    colors = [color for color, count in most_common_colors]
    
    # Convert to hex strings
    hex_colors = [rgb_to_hex(color) for color in colors]
    
    # Sort colors by brightness (luminance)
    def luminance(hex_color):
        rgb = hex_to_rgb(hex_color)
        return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    
    hex_colors.sort(key=luminance)
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in hex_colors:
                f.write(f"{color}\n")
        print(f"Extracted {len(hex_colors)} colors and saved to {output_file}")
    
    return hex_colors

def main():
    parser = argparse.ArgumentParser(description='Extract colors from an image')
    parser.add_argument('--image', required=True, help='Input image file')
    parser.add_argument('--num-colors', type=int, default=50, help='Number of colors to extract')
    parser.add_argument('--output', help='Output palette file')
    
    args = parser.parse_args()
    
    colors = extract_colors_from_image(args.image, args.num_colors, args.output)
    print(f"Extracted {len(colors)} colors from {args.image}")
    
    if not args.output:
        print("Colors found:")
        for color in colors:
            print(color)

if __name__ == '__main__':
    main()
