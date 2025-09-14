#!/usr/bin/env python3
"""
Dithering Module for HyperfckGradients
Adapted from ditherjs library algorithms
"""

import numpy as np
from PIL import Image
from typing import List, Tuple, Union

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def load_palette_from_file(palette_file: str) -> List[Tuple[int, int, int]]:
    """Load palette from file and convert to RGB tuples."""
    palette = []
    with open(palette_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('#'):
                palette.append(hex_to_rgb(line))
    return palette

def find_closest_color(target_color: Tuple[int, int, int], palette: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """Find the closest color in the palette using Euclidean distance."""
    target = np.array(target_color)
    min_distance = float('inf')
    closest_color = palette[0]
    
    for color in palette:
        color_array = np.array(color)
        distance = np.sqrt(np.sum((target - color_array) ** 2))
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    
    return closest_color

def ordered_dither(image: Image.Image, palette: List[Tuple[int, int, int]], step: int = 1) -> Image.Image:
    """
    Apply ordered dithering using a 4x4 Bayer matrix.
    
    Args:
        image: PIL Image to dither
        palette: List of RGB color tuples
        step: Step size for pixel processing
    
    Returns:
        Dithered PIL Image
    """
    # Convert to numpy array
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # Create output array
    output = img_array.copy()
    
    # 4x4 Bayer matrix
    bayer_matrix = np.array([
        [1, 9, 3, 11],
        [13, 5, 15, 7],
        [4, 12, 2, 10],
        [16, 8, 14, 6]
    ])
    
    ratio = 3
    
    for y in range(0, h, step):
        for x in range(0, w, step):
            # Get current pixel color
            current_color = tuple(img_array[y, x])
            
            # Add dithering noise
            noise = bayer_matrix[x % 4, y % 4] * ratio
            dithered_color = tuple(np.clip(np.array(current_color) + noise, 0, 255).astype(int))
            
            # Find closest palette color
            closest_color = find_closest_color(dithered_color, palette)
            
            # Apply color to block
            for dy in range(step):
                for dx in range(step):
                    if y + dy < h and x + dx < w:
                        output[y + dy, x + dx] = closest_color
    
    return Image.fromarray(output)

def floyd_steinberg_dither(image: Image.Image, palette: List[Tuple[int, int, int]], step: int = 1) -> Image.Image:
    """
    Apply Floyd-Steinberg error diffusion dithering.
    
    Args:
        image: PIL Image to dither
        palette: List of RGB color tuples
        step: Step size for pixel processing
    
    Returns:
        Dithered PIL Image
    """
    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32)
    h, w = img_array.shape[:2]
    
    # Create output array
    output = img_array.copy()
    
    for y in range(0, h, step):
        for x in range(0, w, step):
            # Get current pixel color
            current_color = tuple(output[y, x].astype(int))
            
            # Find closest palette color
            closest_color = find_closest_color(current_color, palette)
            
            # Calculate error
            error = np.array(current_color) - np.array(closest_color)
            
            # Apply Floyd-Steinberg error diffusion
            if x + step < w:
                output[y, x + step] += error * 7/16
            if y + step < h:
                if x - step >= 0:
                    output[y + step, x - step] += error * 3/16
                output[y + step, x] += error * 5/16
                if x + step < w:
                    output[y + step, x + step] += error * 1/16
            
            # Set pixel to closest color
            output[y, x] = closest_color
    
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8))

def atkinson_dither(image: Image.Image, palette: List[Tuple[int, int, int]], step: int = 1) -> Image.Image:
    """
    Apply Atkinson error diffusion dithering (used by Apple).
    
    Args:
        image: PIL Image to dither
        palette: List of RGB color tuples
        step: Step size for pixel processing
    
    Returns:
        Dithered PIL Image
    """
    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32)
    h, w = img_array.shape[:2]
    
    # Create output array
    output = img_array.copy()
    
    for y in range(0, h, step):
        for x in range(0, w, step):
            # Get current pixel color
            current_color = tuple(output[y, x].astype(int))
            
            # Find closest palette color
            closest_color = find_closest_color(current_color, palette)
            
            # Calculate error
            error = np.array(current_color) - np.array(closest_color)
            
            # Apply Atkinson error diffusion
            if x + step < w:
                output[y, x + step] += error / 8
            if y + step < h:
                if x - step >= 0:
                    output[y + step, x - step] += error / 8
                output[y + step, x] += error / 8
                if x + step < w:
                    output[y + step, x + step] += error / 8
                if x + 2*step < w:
                    output[y, x + 2*step] += error / 8
                if y + 2*step < h:
                    output[y + 2*step, x] += error / 8
            
            # Set pixel to closest color
            output[y, x] = closest_color
    
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8))

def apply_dithering(image: Image.Image, palette_file: str, algorithm: str = "ordered", step: int = 1) -> Image.Image:
    """
    Apply dithering to an image using the specified algorithm and palette.
    
    Args:
        image: PIL Image to dither
        palette_file: Path to palette file
        algorithm: Dithering algorithm ("ordered", "floyd_steinberg", "atkinson")
        step: Step size for pixel processing
    
    Returns:
        Dithered PIL Image
    """
    # Load palette
    palette = load_palette_from_file(palette_file)
    
    if not palette:
        raise ValueError(f"No valid colors found in palette file: {palette_file}")
    
    # Apply dithering based on algorithm
    if algorithm == "ordered":
        return ordered_dither(image, palette, step)
    elif algorithm == "floyd_steinberg":
        return floyd_steinberg_dither(image, palette, step)
    elif algorithm == "atkinson":
        return atkinson_dither(image, palette, step)
    else:
        raise ValueError(f"Unknown dithering algorithm: {algorithm}")

def main():
    """Command line interface for dithering."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply dithering to an image')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--palette-file', required=True, help='Palette file path')
    parser.add_argument('--algorithm', choices=['ordered', 'floyd_steinberg', 'atkinson'], 
                       default='ordered', help='Dithering algorithm')
    parser.add_argument('--step', type=int, default=1, help='Step size for pixel processing')
    parser.add_argument('--output', required=True, help='Output image file')
    
    args = parser.parse_args()
    
    # Load image
    image = Image.open(args.input)
    
    # Apply dithering
    dithered = apply_dithering(image, args.palette_file, args.algorithm, args.step)
    
    # Save result
    dithered.save(args.output)
    print(f"Dithering applied and saved to {args.output}")

if __name__ == '__main__':
    main()
