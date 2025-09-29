#!/usr/bin/env python3
"""
Grain Processor - Dithering and Grain Effects
Post-processing module for adding grain effects without modifying original wave generation.
"""

import numpy as np
from PIL import Image
import random


def apply_dithering_grain(image: Image.Image, intensity: float = 0.1, 
                         grain_size: float = 1.0, monochrome: bool = False,
                         border_size: int = 0) -> Image.Image:
    """
    Apply dithering-style grain to an image.
    
    Args:
        image: PIL Image to process
        intensity: Grain intensity (0.0 to 1.0)
        grain_size: Size of grain particles (0.5 to 3.0)
        monochrome: If True, apply grain to luminance only
    
    Returns:
        PIL Image with grain applied
    """
    # Convert to numpy array
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create grain pattern
    grain = np.random.normal(0, intensity * 255, (height, width, channels))
    
    # Exclude border from grain if border_size is specified
    if border_size > 0:
        grain[:border_size, :] = 0  # Top border
        grain[-border_size:, :] = 0  # Bottom border
        grain[:, :border_size] = 0  # Left border
        grain[:, -border_size:] = 0  # Right border
    
    # Apply grain size scaling
    if grain_size != 1.0:
        # Simple grain size effect by scaling the noise
        scale_factor = int(grain_size)
        if scale_factor > 1:
            # Upsample grain and downsample
            grain_large = np.repeat(np.repeat(grain, scale_factor, axis=0), scale_factor, axis=1)
            grain = grain_large[:height, :width]
    
    # Apply grain
    result = img_array.astype(np.float32) + grain
    
    # Handle monochrome grain
    if monochrome:
        # Convert to grayscale for grain calculation
        gray = np.dot(result[...,:3], [0.299, 0.587, 0.114])
        gray_grain = np.random.normal(0, intensity * 255, (height, width))
        gray_result = gray + gray_grain
        # Convert back to RGB
        result = np.stack([gray_result, gray_result, gray_result], axis=2)
    
    # Clamp values to valid range
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def apply_bayer_dithering(image: Image.Image, levels: int = 8) -> Image.Image:
    """
    Apply Bayer matrix dithering for retro/digital look.
    
    Args:
        image: PIL Image to process
        levels: Number of color levels (2-256)
    
    Returns:
        PIL Image with Bayer dithering applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create Bayer matrix (4x4)
    bayer_matrix = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ]) / 16.0
    
    # Tile the Bayer matrix across the image
    bayer_tiled = np.tile(bayer_matrix, (height // 4 + 1, width // 4 + 1))
    bayer_tiled = bayer_tiled[:height, :width]
    
    # Apply dithering
    result = img_array.astype(np.float32)
    for c in range(channels):
        channel = result[:, :, c]
        # Add Bayer matrix
        dithered = channel + (bayer_tiled - 0.5) * (255 / levels)
        # Quantize to levels
        dithered = np.round(dithered / (255 / levels)) * (255 / levels)
        result[:, :, c] = dithered
    
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))


def apply_film_grain(image: Image.Image, intensity: float = 0.15, 
                    color_noise: bool = True) -> Image.Image:
    """
    Apply film-style grain with color noise.
    
    Args:
        image: PIL Image to process
        intensity: Grain intensity (0.0 to 1.0)
        color_noise: If True, apply different noise to each channel
    
    Returns:
        PIL Image with film grain applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    if color_noise:
        # Different noise for each channel
        grain = np.random.normal(0, intensity * 255, (height, width, channels))
    else:
        # Same noise for all channels
        grain_base = np.random.normal(0, intensity * 255, (height, width))
        grain = np.stack([grain_base, grain_base, grain_base], axis=2)
    
    # Apply grain
    result = img_array.astype(np.float32) + grain
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def main():
    """Test the grain processor with a sample image."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply grain effects to images')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--output', required=True, help='Output image file')
    parser.add_argument('--grain-type', choices=['dithering', 'bayer', 'film'], 
                       default='dithering', help='Type of grain to apply')
    parser.add_argument('--intensity', type=float, default=0.1, 
                       help='Grain intensity (0.0-1.0)')
    parser.add_argument('--grain-size', type=float, default=1.0, 
                       help='Grain size (0.5-3.0)')
    parser.add_argument('--monochrome', action='store_true', 
                       help='Apply grain to luminance only')
    parser.add_argument('--border-size', type=int, default=0, 
                       help='Border size to exclude from grain (0 = no exclusion)')
    parser.add_argument('--levels', type=int, default=8, 
                       help='Color levels for Bayer dithering')
    
    args = parser.parse_args()
    
    # Load image
    image = Image.open(args.input)
    
    # Apply grain based on type
    if args.grain_type == 'dithering':
        result = apply_dithering_grain(image, args.intensity, args.grain_size, args.monochrome, args.border_size)
    elif args.grain_type == 'bayer':
        result = apply_bayer_dithering(image, args.levels)
    elif args.grain_type == 'film':
        result = apply_film_grain(image, args.intensity, not args.monochrome)
    
    # Save result
    result.save(args.output)
    print(f"Grain applied and saved as '{args.output}'")


if __name__ == '__main__':
    main()
