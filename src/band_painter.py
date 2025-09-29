#!/usr/bin/env python3
"""
Band Painter - Artistic Effects for Gradient Bands
Post-processing module for applying painting effects to gradient bands.
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import random
import math


def apply_crayon_effect(image: Image.Image, intensity: float = 0.3, 
                        roughness: float = 0.5, border_size: int = 0) -> Image.Image:
    """
    Apply crayon-like effect to gradient bands.
    
    Args:
        image: PIL Image to process
        intensity: Effect intensity (0.0 to 1.0)
        roughness: Edge roughness (0.0 to 1.0)
        border_size: Border size to exclude from effect
    
    Returns:
        PIL Image with crayon effect applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create crayon texture with much stronger effect
    crayon_texture = np.random.normal(0, intensity * 100, (height, width, channels))
    
    # Exclude border if specified
    if border_size > 0:
        crayon_texture[:border_size, :] = 0
        crayon_texture[-border_size:, :] = 0
        crayon_texture[:, :border_size] = 0
        crayon_texture[:, -border_size:] = 0
    
    # Add roughness to band edges
    if roughness > 0:
        # Create edge noise
        edge_noise = np.random.normal(0, roughness * 60, (height, width, channels))
        crayon_texture += edge_noise
    
    # Apply crayon effect
    result = img_array.astype(np.float32) + crayon_texture
    
    # Add slight color bleeding between bands
    bleeding = np.random.normal(0, intensity * 40, (height, width, channels))
    result += bleeding
    
    # Clamp values
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def apply_pencil_effect(image: Image.Image, intensity: float = 0.4, 
                       stroke_direction: str = 'horizontal', border_size: int = 0) -> Image.Image:
    """
    Apply pencil/crayon stroke effect to gradient bands.
    
    Args:
        image: PIL Image to process
        intensity: Effect intensity (0.0 to 1.0)
        stroke_direction: 'horizontal', 'vertical', or 'diagonal'
        border_size: Border size to exclude from effect
    
    Returns:
        PIL Image with pencil effect applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create pencil strokes
    strokes = np.zeros((height, width, channels))
    
    if stroke_direction == 'horizontal':
        # Horizontal pencil strokes
        for y in range(0, height, 3):  # Every 3 pixels
            stroke_intensity = np.random.normal(0, intensity * 40, width)
            for c in range(channels):
                strokes[y:y+2, :, c] += stroke_intensity
    elif stroke_direction == 'vertical':
        # Vertical pencil strokes
        for x in range(0, width, 3):
            stroke_intensity = np.random.normal(0, intensity * 40, height)
            for c in range(channels):
                strokes[:, x:x+2, c] += stroke_intensity
    elif stroke_direction == 'diagonal':
        # Diagonal pencil strokes
        for i in range(0, max(height, width), 4):
            stroke_intensity = np.random.normal(0, intensity * 30)
            for c in range(channels):
                # Create diagonal strokes
                for j in range(min(3, height-i), min(3, width-i)):
                    if i+j < height and j < width:
                        strokes[i+j, j, c] += stroke_intensity
    
    # Exclude border if specified
    if border_size > 0:
        strokes[:border_size, :] = 0
        strokes[-border_size:, :] = 0
        strokes[:, :border_size] = 0
        strokes[:, -border_size:] = 0
    
    # Apply pencil effect
    result = img_array.astype(np.float32) + strokes
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def apply_watercolor_effect(image: Image.Image, intensity: float = 0.3, 
                           bleeding: float = 0.4, border_size: int = 0) -> Image.Image:
    """
    Apply watercolor-like effect to gradient bands.
    
    Args:
        image: PIL Image to process
        intensity: Effect intensity (0.0 to 1.0)
        bleeding: Color bleeding amount (0.0 to 1.0)
        border_size: Border size to exclude from effect
    
    Returns:
        PIL Image with watercolor effect applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create watercolor bleeding effect
    watercolor_noise = np.random.normal(0, intensity * 30, (height, width, channels))
    
    # Add color bleeding between bands
    if bleeding > 0:
        # Create soft edges
        soft_edges = np.random.normal(0, bleeding * 25, (height, width, channels))
        watercolor_noise += soft_edges
    
    # Exclude border if specified
    if border_size > 0:
        watercolor_noise[:border_size, :] = 0
        watercolor_noise[-border_size:, :] = 0
        watercolor_noise[:, :border_size] = 0
        watercolor_noise[:, -border_size:] = 0
    
    # Apply watercolor effect
    result = img_array.astype(np.float32) + watercolor_noise
    
    # Add slight blur for watercolor feel
    if intensity > 0.2:
        # Convert to PIL for blur
        temp_img = Image.fromarray(result.astype(np.uint8))
        temp_img = temp_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        result = np.array(temp_img)
    
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def apply_oil_paint_effect(image: Image.Image, intensity: float = 0.4, 
                          brush_size: float = 2.0, border_size: int = 0) -> Image.Image:
    """
    Apply oil paint-like effect to gradient bands.
    
    Args:
        image: PIL Image to process
        intensity: Effect intensity (0.0 to 1.0)
        brush_size: Brush stroke size (1.0 to 4.0)
        border_size: Border size to exclude from effect
    
    Returns:
        PIL Image with oil paint effect applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create oil paint texture
    oil_texture = np.random.normal(0, intensity * 40, (height, width, channels))
    
    # Add brush stroke effects
    brush_strokes = np.zeros((height, width, channels))
    stroke_size = int(brush_size)
    
    for _ in range(int(intensity * 100)):  # Number of brush strokes
        # Random brush stroke
        start_x = random.randint(0, width-1)
        start_y = random.randint(0, height-1)
        length = random.randint(10, 30)
        angle = random.uniform(0, 2 * math.pi)
        
        for i in range(length):
            x = int(start_x + i * math.cos(angle))
            y = int(start_y + i * math.sin(angle))
            
            if 0 <= x < width and 0 <= y < height:
                stroke_intensity = random.uniform(-intensity * 30, intensity * 30)
                for c in range(channels):
                    brush_strokes[y:y+stroke_size, x:x+stroke_size, c] += stroke_intensity
    
    # Exclude border if specified
    if border_size > 0:
        oil_texture[:border_size, :] = 0
        oil_texture[-border_size:, :] = 0
        oil_texture[:, :border_size] = 0
        oil_texture[:, -border_size:] = 0
        brush_strokes[:border_size, :] = 0
        brush_strokes[-border_size:, :] = 0
        brush_strokes[:, :border_size] = 0
        brush_strokes[:, -border_size:] = 0
    
    # Apply oil paint effect
    result = img_array.astype(np.float32) + oil_texture + brush_strokes
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def main():
    """Test the band painter with a sample image."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply painting effects to gradient bands')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--output', required=True, help='Output image file')
    parser.add_argument('--effect', choices=['crayon', 'pencil', 'watercolor', 'oil'], 
                       default='crayon', help='Type of painting effect')
    parser.add_argument('--intensity', type=float, default=0.3, 
                       help='Effect intensity (0.0-1.0)')
    parser.add_argument('--border-size', type=int, default=0, 
                       help='Border size to exclude from effect')
    parser.add_argument('--roughness', type=float, default=0.5, 
                       help='Edge roughness for crayon effect')
    parser.add_argument('--stroke-direction', choices=['horizontal', 'vertical', 'diagonal'], 
                       default='horizontal', help='Stroke direction for pencil effect')
    parser.add_argument('--bleeding', type=float, default=0.4, 
                       help='Color bleeding for watercolor effect')
    parser.add_argument('--brush-size', type=float, default=2.0, 
                       help='Brush size for oil paint effect')
    
    args = parser.parse_args()
    
    # Load image
    image = Image.open(args.input)
    
    # Apply effect based on type
    if args.effect == 'crayon':
        result = apply_crayon_effect(image, args.intensity, args.roughness, args.border_size)
    elif args.effect == 'pencil':
        result = apply_pencil_effect(image, args.intensity, args.stroke_direction, args.border_size)
    elif args.effect == 'watercolor':
        result = apply_watercolor_effect(image, args.intensity, args.bleeding, args.border_size)
    elif args.effect == 'oil':
        result = apply_oil_paint_effect(image, args.intensity, args.brush_size, args.border_size)
    
    # Save result
    result.save(args.output)
    print(f"Painting effect applied and saved as '{args.output}'")


if __name__ == '__main__':
    main()
