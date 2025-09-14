#!/usr/bin/env python3
"""
Create high-contrast palettes by selecting every Nth color from existing palettes.
"""

import argparse

def create_high_contrast_palette(input_file: str, output_file: str, step: int = 5):
    """
    Create a high-contrast palette by selecting every Nth color.
    
    Args:
        input_file: Input palette file
        output_file: Output palette file
        step: Step size (every Nth color)
    """
    colors = []
    
    # Read all colors
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('#'):
                colors.append(line)
    
    # Select every Nth color
    high_contrast_colors = []
    for i in range(0, len(colors), step):
        high_contrast_colors.append(colors[i])
    
    # Always include the last color
    if colors and colors[-1] not in high_contrast_colors:
        high_contrast_colors.append(colors[-1])
    
    # Save high-contrast palette
    with open(output_file, 'w') as f:
        for color in high_contrast_colors:
            f.write(f"{color}\n")
    
    print(f"Created high-contrast palette with {len(high_contrast_colors)} colors")
    print(f"Selected every {step}th color from {len(colors)} total colors")
    print(f"Saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Create high-contrast palettes')
    parser.add_argument('--input', required=True, help='Input palette file')
    parser.add_argument('--output', required=True, help='Output palette file')
    parser.add_argument('--step', type=int, default=5, help='Step size (every Nth color)')
    
    args = parser.parse_args()
    
    create_high_contrast_palette(args.input, args.output, args.step)

if __name__ == '__main__':
    main()
