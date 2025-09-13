#!/usr/bin/env python3
"""
Color Extraction Tool
Extracts a specified number of colors from an image using K-means clustering.
"""

import argparse
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

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
    
    # Resize image for faster processing (optional)
    img = img.resize((150, 150))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Reshape to list of pixels
    pixels = img_array.reshape(-1, 3)
    
    # Use K-means to find the most representative colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get the cluster centers (colors)
    colors = kmeans.cluster_centers_.astype(int)
    
    # Convert to hex strings
    hex_colors = []
    for color in colors:
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        hex_colors.append(hex_color)
    
    # Sort colors by brightness (optional)
    hex_colors.sort(key=lambda x: sum(int(x[i:i+2], 16) for i in (1, 3, 5)))
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            for color in hex_colors:
                f.write(f"{color}\n")
        print(f"Extracted {num_colors} colors and saved to {output_file}")
    
    return hex_colors

def expand_palette(original_colors, target_count=50):
    """
    Expand an existing palette by interpolating between colors.
    
    Args:
        original_colors: List of hex color strings
        target_count: Target number of colors
    
    Returns:
        List of expanded hex color strings
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    # Convert to RGB
    rgb_colors = [hex_to_rgb(color) for color in original_colors]
    
    # Create expanded palette
    expanded_colors = []
    
    # Calculate how many colors to generate between each pair
    colors_per_interval = target_count // (len(rgb_colors) - 1)
    remainder = target_count % (len(rgb_colors) - 1)
    
    for i in range(len(rgb_colors) - 1):
        start_color = rgb_colors[i]
        end_color = rgb_colors[i + 1]
        
        # Add the start color
        expanded_colors.append(rgb_to_hex(start_color))
        
        # Generate intermediate colors
        num_intermediates = colors_per_interval + (1 if i < remainder else 0)
        
        for j in range(1, num_intermediates):
            ratio = j / num_intermediates
            interpolated = tuple(
                int(start_color[k] + ratio * (end_color[k] - start_color[k]))
                for k in range(3)
            )
            expanded_colors.append(rgb_to_hex(interpolated))
    
    # Add the last color
    expanded_colors.append(rgb_to_hex(rgb_colors[-1]))
    
    return expanded_colors

def main():
    parser = argparse.ArgumentParser(description='Extract colors from an image')
    parser.add_argument('--image', help='Input image file')
    parser.add_argument('--palette-file', help='Input palette file (for expansion)')
    parser.add_argument('--num-colors', type=int, default=50, help='Number of colors to extract')
    parser.add_argument('--output', help='Output palette file')
    parser.add_argument('--mode', choices=['extract', 'expand'], default='extract',
                       help='Mode: extract from image or expand existing palette')
    
    args = parser.parse_args()
    
    if args.mode == 'extract':
        if not args.image:
            print("Error: --image required for extract mode")
            return
        
        colors = extract_colors_from_image(args.image, args.num_colors, args.output)
        print(f"Extracted {len(colors)} colors from {args.image}")
        
    elif args.mode == 'expand':
        if not args.palette_file:
            print("Error: --palette-file required for expand mode")
            return
        
        # Read existing palette
        with open(args.palette_file, 'r') as f:
            original_colors = [line.strip() for line in f if line.strip()]
        
        # Expand palette
        expanded_colors = expand_palette(original_colors, args.num_colors)
        
        # Save expanded palette
        if args.output:
            with open(args.output, 'w') as f:
                for color in expanded_colors:
                    f.write(f"{color}\n")
            print(f"Expanded palette from {len(original_colors)} to {len(expanded_colors)} colors")
            print(f"Saved to {args.output}")
        else:
            print(f"Expanded palette from {len(original_colors)} to {len(expanded_colors)} colors")
            for color in expanded_colors:
                print(color)

if __name__ == '__main__':
    main()

