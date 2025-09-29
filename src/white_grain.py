#!/usr/bin/env python3
"""
White Grain Generator
Creates random white grain patterns with varying density and size.
"""

import numpy as np
from PIL import Image
import random
import math


def apply_white_grain(image: Image.Image, base_intensity: float = 0.1, 
                      density_variation: float = 0.5, size_variation: float = 0.8,
                      border_size: int = 0) -> Image.Image:
    """
    Apply random white grain with varying density and size.
    
    Args:
        image: PIL Image to process
        base_intensity: Base grain intensity (0.0 to 1.0)
        density_variation: How much density varies across image (0.0 to 1.0)
        size_variation: How much grain size varies (0.0 to 1.0)
        border_size: Border size to exclude from grain
    
    Returns:
        PIL Image with white grain applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create white grain pattern
    white_grain = np.zeros((height, width, channels))
    
    # Work only on the gradient area (exclude borders)
    start_y = border_size
    end_y = height - border_size
    start_x = border_size
    end_x = width - border_size
    
    if start_y >= end_y or start_x >= end_x:
        return image
    
    # Generate random grain with varying density and size
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            # Random density variation across the image
            density_factor = 1.0 + density_variation * (random.random() - 0.5) * 2
            
            # Random size variation
            size_factor = 1.0 + size_variation * (random.random() - 0.5) * 2
            
            # Calculate grain intensity for this pixel
            grain_intensity = base_intensity * density_factor * size_factor
            
            # Generate white grain
            if random.random() < grain_intensity:
                # Random grain size (1x1 to 3x3 pixels)
                grain_size = max(1, int(size_factor * 2))
                
                # Add white grain
                for dy in range(grain_size):
                    for dx in range(grain_size):
                        gy = min(y + dy, end_y - 1)
                        gx = min(x + dx, end_x - 1)
                        
                        # White grain intensity
                        white_value = random.uniform(50, 255)
                        white_grain[gy, gx] = [white_value, white_value, white_value]
    
    # Apply white grain to image
    result = img_array.astype(np.float32) + white_grain.astype(np.float32)
    result = np.clip(result, 0, 255)
    
    return Image.fromarray(result.astype(np.uint8))


def apply_scattered_white_grain(image: Image.Image, num_grains: int = 1000,
                               min_size: int = 1, max_size: int = 5,
                               border_size: int = 0) -> Image.Image:
    """
    Apply scattered white grain particles of random sizes.
    
    Args:
        image: PIL Image to process
        num_grains: Number of grain particles to add
        min_size: Minimum grain particle size
        max_size: Maximum grain particle size
        border_size: Border size to exclude from grain
    
    Returns:
        PIL Image with scattered white grain applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Work only on the gradient area (exclude borders)
    start_y = border_size
    end_y = height - border_size
    start_x = border_size
    end_x = width - border_size
    
    if start_y >= end_y or start_x >= end_x:
        return image
    
    # Create white grain particles
    for _ in range(num_grains):
        # Random position
        x = random.randint(start_x, end_x - 1)
        y = random.randint(start_y, end_y - 1)
        
        # Random size
        size = random.randint(min_size, max_size)
        
        # Random intensity
        intensity = random.uniform(100, 255)
        
        # Add grain particle
        for dy in range(size):
            for dx in range(size):
                gy = min(y + dy, end_y - 1)
                gx = min(x + dx, end_x - 1)
                
                # Add white grain
                img_array[gy, gx] = [intensity, intensity, intensity]
    
    return Image.fromarray(img_array.astype(np.uint8))


def apply_clustered_white_grain(image: Image.Image, num_clusters: int = 50,
                               cluster_size: int = 20, grain_density: float = 0.3,
                               border_size: int = 0) -> Image.Image:
    """
    Apply clustered white grain patterns.
    
    Args:
        image: PIL Image to process
        num_clusters: Number of grain clusters
        cluster_size: Size of each cluster
        grain_density: Density of grains within clusters
        border_size: Border size to exclude from grain
    
    Returns:
        PIL Image with clustered white grain applied
    """
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Work only on the gradient area (exclude borders)
    start_y = border_size
    end_y = height - border_size
    start_x = border_size
    end_x = width - border_size
    
    if start_y >= end_y or start_x >= end_x:
        return image
    
    # Create grain clusters
    for _ in range(num_clusters):
        # Random cluster center
        center_x = random.randint(start_x, end_x - 1)
        center_y = random.randint(start_y, end_y - 1)
        
        # Add grains around cluster center
        for _ in range(int(cluster_size * grain_density)):
            # Random offset from center
            offset_x = random.randint(-cluster_size//2, cluster_size//2)
            offset_y = random.randint(-cluster_size//2, cluster_size//2)
            
            gx = center_x + offset_x
            gy = center_y + offset_y
            
            # Check bounds
            if start_x <= gx < end_x and start_y <= gy < end_y:
                # Random white intensity
                intensity = random.uniform(80, 255)
                img_array[gy, gx] = [intensity, intensity, intensity]
    
    return Image.fromarray(img_array.astype(np.uint8))


def main():
    """Test the white grain generator with a sample image."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply white grain effects to images')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--output', required=True, help='Output image file')
    parser.add_argument('--grain-type', choices=['random', 'scattered', 'clustered'], 
                       default='random', help='Type of white grain')
    parser.add_argument('--base-intensity', type=float, default=0.1, 
                       help='Base grain intensity (0.0-1.0)')
    parser.add_argument('--density-variation', type=float, default=0.5, 
                       help='Density variation (0.0-1.0)')
    parser.add_argument('--size-variation', type=float, default=0.8, 
                       help='Size variation (0.0-1.0)')
    parser.add_argument('--border-size', type=int, default=0, 
                       help='Border size to exclude from grain')
    parser.add_argument('--num-grains', type=int, default=1000, 
                       help='Number of grains for scattered type')
    parser.add_argument('--min-size', type=int, default=1, 
                       help='Minimum grain size')
    parser.add_argument('--max-size', type=int, default=5, 
                       help='Maximum grain size')
    parser.add_argument('--num-clusters', type=int, default=50, 
                       help='Number of clusters for clustered type')
    parser.add_argument('--cluster-size', type=int, default=20, 
                       help='Size of each cluster')
    parser.add_argument('--grain-density', type=float, default=0.3, 
                       help='Density of grains within clusters')
    
    args = parser.parse_args()
    
    # Load image
    image = Image.open(args.input)
    
    # Apply grain based on type
    if args.grain_type == 'random':
        result = apply_white_grain(image, args.base_intensity, args.density_variation, 
                                 args.size_variation, args.border_size)
    elif args.grain_type == 'scattered':
        result = apply_scattered_white_grain(image, args.num_grains, args.min_size, 
                                           args.max_size, args.border_size)
    elif args.grain_type == 'clustered':
        result = apply_clustered_white_grain(image, args.num_clusters, args.cluster_size, 
                                           args.grain_density, args.border_size)
    
    # Save result
    result.save(args.output)
    print(f"White grain applied and saved as '{args.output}'")


if __name__ == '__main__':
    main()





