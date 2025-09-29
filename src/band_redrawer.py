#!/usr/bin/env python3
"""
Band Redrawer - Artistic Band Redrawing
Takes existing wave images and redraws the bands with artistic texture.
Does not modify original wave generation code.
"""

import numpy as np
from PIL import Image, ImageFilter
import random
import math


def detect_bands(image: Image.Image, border_size: int = 0) -> list:
    """
    Detect band boundaries in a gradient image.
    
    Args:
        image: PIL Image with gradient bands
        border_size: Border size to exclude from detection
    
    Returns:
        List of band boundaries (y coordinates)
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Work only on the gradient area (exclude borders)
    start_y = border_size
    end_y = height - border_size
    start_x = border_size
    end_x = width - border_size
    
    if start_y >= end_y or start_x >= end_x:
        return []
    
    # Sample a column in the middle to detect bands
    sample_x = start_x + (end_x - start_x) // 2
    sample_column = img_array[start_y:end_y, sample_x, :]
    
    # Find color changes (band boundaries)
    band_boundaries = []
    prev_color = sample_column[0]
    
    for y in range(1, len(sample_column)):
        current_color = sample_column[y]
        # Calculate color difference
        color_diff = np.sum(np.abs(current_color.astype(float) - prev_color.astype(float)))
        
        if color_diff > 30:  # Significant color change
            band_boundaries.append(start_y + y)
            prev_color = current_color
    
    return band_boundaries


def redraw_bands_crayon(image: Image.Image, intensity: float = 0.5, 
                        roughness: float = 0.7, border_size: int = 0) -> Image.Image:
    """
    Redraw gradient bands with crayon-like texture.
    
    Args:
        image: PIL Image with gradient bands
        intensity: Crayon effect intensity (0.0 to 1.0)
        roughness: Edge roughness (0.0 to 1.0)
        border_size: Border size to exclude from redrawing
    
    Returns:
        PIL Image with crayon-redrawn bands
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Detect band boundaries
    band_boundaries = detect_bands(image, border_size)
    
    if not band_boundaries:
        # Fallback: create bands based on height
        num_bands = 20  # Default number of bands
        band_height = (height - 2 * border_size) // num_bands
        band_boundaries = [border_size + i * band_height for i in range(1, num_bands)]
    
    # Create new image
    result = np.copy(img_array)
    
    # Redraw each band with crayon texture
    for i in range(len(band_boundaries) + 1):
        # Determine band boundaries
        if i == 0:
            start_y = border_size
        else:
            start_y = band_boundaries[i-1]
        
        if i == len(band_boundaries):
            end_y = height - border_size
        else:
            end_y = band_boundaries[i]
        
        if start_y >= end_y:
            continue
        
        # Get the average color of this band
        band_region = img_array[start_y:end_y, border_size:width-border_size, :]
        avg_color = np.mean(band_region, axis=(0, 1))
        
        # Add crayon texture to this band
        for y in range(start_y, end_y):
            for x in range(border_size, width - border_size):
                # Crayon texture: irregular, waxy
                crayon_noise = np.random.normal(0, intensity * 50, channels)
                
                # Add roughness to edges
                edge_factor = 1.0
                if y - start_y < 5 or end_y - y < 5:  # Near band edges
                    edge_factor = 1.0 + roughness * np.random.normal(0, 0.3)
                
                # Apply crayon effect
                new_color = avg_color + crayon_noise * edge_factor
                new_color = np.clip(new_color, 0, 255)
                
                result[y, x] = new_color
    
    return Image.fromarray(result.astype(np.uint8))


def redraw_bands_pencil(image: Image.Image, intensity: float = 0.6, 
                       stroke_direction: str = 'horizontal', border_size: int = 0) -> Image.Image:
    """
    Redraw gradient bands with pencil-like strokes.
    
    Args:
        image: PIL Image with gradient bands
        intensity: Pencil effect intensity (0.0 to 1.0)
        stroke_direction: 'horizontal', 'vertical', or 'diagonal'
        border_size: Border size to exclude from redrawing
    
    Returns:
        PIL Image with pencil-redrawn bands
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Detect band boundaries
    band_boundaries = detect_bands(image, border_size)
    
    if not band_boundaries:
        # Fallback: create bands based on height
        num_bands = 20
        band_height = (height - 2 * border_size) // num_bands
        band_boundaries = [border_size + i * band_height for i in range(1, num_bands)]
    
    # Create new image
    result = np.copy(img_array)
    
    # Redraw each band with pencil strokes
    for i in range(len(band_boundaries) + 1):
        # Determine band boundaries
        if i == 0:
            start_y = border_size
        else:
            start_y = band_boundaries[i-1]
        
        if i == len(band_boundaries):
            end_y = height - border_size
        else:
            end_y = band_boundaries[i]
        
        if start_y >= end_y:
            continue
        
        # Get the average color of this band
        band_region = img_array[start_y:end_y, border_size:width-border_size, :]
        avg_color = np.mean(band_region, axis=(0, 1))
        
        # Add pencil strokes to this band
        for y in range(start_y, end_y):
            for x in range(border_size, width - border_size):
                # Pencil stroke texture
                stroke_intensity = 0
                
                if stroke_direction == 'horizontal':
                    # Horizontal pencil strokes
                    if (y - start_y) % 3 == 0:  # Every 3rd row
                        stroke_intensity = np.random.normal(0, intensity * 40)
                elif stroke_direction == 'vertical':
                    # Vertical pencil strokes
                    if (x - border_size) % 3 == 0:  # Every 3rd column
                        stroke_intensity = np.random.normal(0, intensity * 40)
                elif stroke_direction == 'diagonal':
                    # Diagonal pencil strokes
                    if (x + y) % 4 == 0:
                        stroke_intensity = np.random.normal(0, intensity * 30)
                
                # Apply pencil effect
                new_color = avg_color + stroke_intensity
                new_color = np.clip(new_color, 0, 255)
                
                result[y, x] = new_color
    
    return Image.fromarray(result.astype(np.uint8))


def redraw_bands_watercolor(image: Image.Image, intensity: float = 0.4, 
                           bleeding: float = 0.6, border_size: int = 0) -> Image.Image:
    """
    Redraw gradient bands with watercolor-like bleeding.
    
    Args:
        image: PIL Image with gradient bands
        intensity: Watercolor effect intensity (0.0 to 1.0)
        bleeding: Color bleeding amount (0.0 to 1.0)
        border_size: Border size to exclude from redrawing
    
    Returns:
        PIL Image with watercolor-redrawn bands
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Detect band boundaries
    band_boundaries = detect_bands(image, border_size)
    
    if not band_boundaries:
        # Fallback: create bands based on height
        num_bands = 20
        band_height = (height - 2 * border_size) // num_bands
        band_boundaries = [border_size + i * band_height for i in range(1, num_bands)]
    
    # Create new image
    result = np.copy(img_array)
    
    # Redraw each band with watercolor bleeding
    for i in range(len(band_boundaries) + 1):
        # Determine band boundaries
        if i == 0:
            start_y = border_size
        else:
            start_y = band_boundaries[i-1]
        
        if i == len(band_boundaries):
            end_y = height - border_size
        else:
            end_y = band_boundaries[i]
        
        if start_y >= end_y:
            continue
        
        # Get the average color of this band
        band_region = img_array[start_y:end_y, border_size:width-border_size, :]
        avg_color = np.mean(band_region, axis=(0, 1))
        
        # Add watercolor bleeding to this band
        for y in range(start_y, end_y):
            for x in range(border_size, width - border_size):
                # Watercolor bleeding effect
                bleeding_noise = np.random.normal(0, intensity * 30, channels)
                
                # Add color bleeding at edges
                edge_bleeding = 0
                if y - start_y < 3 or end_y - y < 3:  # Near band edges
                    edge_bleeding = np.random.normal(0, bleeding * 25, channels)
                
                # Apply watercolor effect
                new_color = avg_color + bleeding_noise + edge_bleeding
                new_color = np.clip(new_color, 0, 255)
                
                result[y, x] = new_color
    
    return Image.fromarray(result.astype(np.uint8))


def main():
    """Test the band redrawer with a sample image."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Redraw gradient bands with artistic texture')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--output', required=True, help='Output image file')
    parser.add_argument('--effect', choices=['crayon', 'pencil', 'watercolor'], 
                       default='crayon', help='Type of artistic effect')
    parser.add_argument('--intensity', type=float, default=0.5, 
                       help='Effect intensity (0.0-1.0)')
    parser.add_argument('--border-size', type=int, default=0, 
                       help='Border size to exclude from redrawing')
    parser.add_argument('--roughness', type=float, default=0.7, 
                       help='Edge roughness for crayon effect')
    parser.add_argument('--stroke-direction', choices=['horizontal', 'vertical', 'diagonal'], 
                       default='horizontal', help='Stroke direction for pencil effect')
    parser.add_argument('--bleeding', type=float, default=0.6, 
                       help='Color bleeding for watercolor effect')
    
    args = parser.parse_args()
    
    # Load image
    image = Image.open(args.input)
    
    # Apply effect based on type
    if args.effect == 'crayon':
        result = redraw_bands_crayon(image, args.intensity, args.roughness, args.border_size)
    elif args.effect == 'pencil':
        result = redraw_bands_pencil(image, args.intensity, args.stroke_direction, args.border_size)
    elif args.effect == 'watercolor':
        result = redraw_bands_watercolor(image, args.intensity, args.bleeding, args.border_size)
    
    # Save result
    result.save(args.output)
    print(f"Bands redrawn with {args.effect} effect and saved as '{args.output}'")


if __name__ == '__main__':
    main()





