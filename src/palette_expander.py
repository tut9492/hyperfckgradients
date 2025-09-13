#!/usr/bin/env python3
"""
Simple Palette Expansion Tool
Expands an existing palette by interpolating between colors.
"""

import argparse

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def expand_palette(original_colors, target_count=50):
    """
    Expand an existing palette by interpolating between colors.
    
    Args:
        original_colors: List of hex color strings
        target_count: Target number of colors
    
    Returns:
        List of expanded hex color strings
    """
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
    parser = argparse.ArgumentParser(description='Expand a color palette')
    parser.add_argument('--palette-file', required=True, help='Input palette file')
    parser.add_argument('--num-colors', type=int, default=50, help='Number of colors to generate')
    parser.add_argument('--output', help='Output palette file')
    
    args = parser.parse_args()
    
    # Read existing palette
    with open(args.palette_file, 'r') as f:
        original_colors = [line.strip() for line in f if line.strip()]
    
    print(f"Original palette has {len(original_colors)} colors")
    
    # Expand palette
    expanded_colors = expand_palette(original_colors, args.num_colors)
    
    # Save expanded palette
    if args.output:
        with open(args.output, 'w') as f:
            for color in expanded_colors:
                f.write(f"{color}\n")
        print(f"Expanded palette to {len(expanded_colors)} colors")
        print(f"Saved to {args.output}")
    else:
        print(f"Expanded palette to {len(expanded_colors)} colors")
        for color in expanded_colors:
            print(color)

if __name__ == '__main__':
    main()

