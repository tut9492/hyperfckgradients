#!/usr/bin/env python3
"""
Gradient Image Generator

A Python script that generates large gradient images from a list of hex colors.
Supports chunky (stepped) gradients with grain effects.

Usage:
    python gradient.py --mode chunky --steps 8 --width 1000 --height 2000
"""

import argparse
from typing import List, Tuple
from PIL import Image
import numpy as np


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def generate_wave_gradient(width: int, height: int, colors: List[str], steps: int,
                          wave_amplitude: float = 0.1, wave_frequency: float = 2.0, 
                          orientation: str = 'horizontal', border: int = 0, border_color: str = None) -> Image.Image:
    """Generate a gradient with wave-like band shifting."""
    grad_width = width - 2 * border
    grad_height = height - 2 * border
    
    if grad_width <= 0 or grad_height <= 0:
        raise ValueError("Border too large for image dimensions")
    
    # Helper to average a slice of the provided palette evenly per step
    def average_palette_slice(start_idx: int, end_idx: int) -> Tuple[int, int, int]:
        end_idx = max(start_idx + 1, end_idx)
        slice_colors = colors[start_idx:end_idx]
        rs = 0
        gs = 0
        bs = 0
        for color in slice_colors:
            r, g, b = hex_to_rgb(color)
            rs += r
            gs += g
            bs += b
        count = len(slice_colors)
        return (rs // count, gs // count, bs // count)
    
    # Calculate how many colors to average per step for even distribution
    colors_per_step = len(colors) / steps
    
    if orientation == 'horizontal':
        gradient = np.zeros((grad_height, grad_width, 3), dtype=np.uint8)
        
        # Create wave function for each column
        x_coords = np.arange(grad_width)
        x_norm = x_coords / grad_width
        
        # Create gradual wave intensity - fade in from edges
        # Use a bell curve or similar function to make wave stronger in center
        center_distance = np.abs(x_norm - 0.5) * 2  # 0 at center, 1 at edges
        wave_intensity = 1 - center_distance  # 1 at center, 0 at edges
        wave_intensity = wave_intensity ** 2  # Make the fade more gradual
        
        wave_shift = wave_amplitude * np.sin(2 * np.pi * wave_frequency * x_norm) * wave_intensity
        
        for step in range(steps):
            # Calculate which slice of the palette to use for this step
            start_color_idx = int(step * colors_per_step)
            end_color_idx = int((step + 1) * colors_per_step)
            avg_color = average_palette_slice(start_color_idx, end_color_idx)
            
            # Calculate the base y position for this step
            base_y_start = int((step / steps) * grad_height)
            base_y_end = int(((step + 1) / steps) * grad_height)
            
            # Apply wave displacement to each column
            for x in range(grad_width):
                # Calculate the wave offset for this column
                wave_offset = int(wave_shift[x] * grad_height)
                
                # Calculate the actual y positions for this column
                y_start = base_y_start + wave_offset
                y_end = base_y_end + wave_offset
                
                # Clamp to valid range
                y_start = max(0, min(grad_height - 1, y_start))
                y_end = max(0, min(grad_height, y_end))
                
                # Fill the band for this column
                if y_end > y_start:
                    gradient[y_start:y_end, x] = avg_color
        
        # Fill any remaining black areas with the appropriate gradient colors
        for x in range(grad_width):
            for y in range(grad_height):
                if np.all(gradient[y, x] == 0):  # If pixel is black (unfilled)
                    # Determine which step this pixel should belong to
                    normalized_y = y / grad_height
                    step = int(normalized_y * steps)
                    step = max(0, min(steps - 1, step))
                    
                    # Get the color for this step
                    start_color_idx = int(step * colors_per_step)
                    end_color_idx = int((step + 1) * colors_per_step)
                    avg_color = average_palette_slice(start_color_idx, end_color_idx)
                    
                    gradient[y, x] = avg_color
        
        # Ensure the very top and bottom rows are completely filled with correct colors
        for x in range(grad_width):
            # Fill top row with first color (darkest purple)
            gradient[0, x] = average_palette_slice(0, int(colors_per_step))
            # Fill bottom row with last color (lightest purple)
            gradient[grad_height-1, x] = average_palette_slice(int((steps-1) * colors_per_step), len(colors))
        
        # Fill any remaining gaps with the correct gradient colors
        for x in range(grad_width):
            for y in range(grad_height):
                if np.all(gradient[y, x] == 0):  # If pixel is still black (unfilled)
                    # Determine which step this pixel should belong to based on its y position
                    normalized_y = y / grad_height
                    step = int(normalized_y * steps)
                    step = max(0, min(steps - 1, step))
                    
                    # Get the color for this step
                    start_color_idx = int(step * colors_per_step)
                    end_color_idx = int((step + 1) * colors_per_step)
                    avg_color = average_palette_slice(start_color_idx, end_color_idx)
                    
                    gradient[y, x] = avg_color
                    
    else:  # vertical - similar but with x displacement
        gradient = np.zeros((grad_height, grad_width, 3), dtype=np.uint8)
        
        # Create wave function for each row
        y_coords = np.arange(grad_height)
        y_norm = y_coords / grad_height
        
        # Create gradual wave intensity - fade in from edges
        center_distance = np.abs(y_norm - 0.5) * 2  # 0 at center, 1 at edges
        wave_intensity = 1 - center_distance  # 1 at center, 0 at edges
        wave_intensity = wave_intensity ** 2  # Make the fade more gradual
        
        wave_shift = wave_amplitude * np.sin(2 * np.pi * wave_frequency * y_norm) * wave_intensity
        
        for step in range(steps):
            # Calculate which slice of the palette to use for this step
            start_color_idx = int(step * colors_per_step)
            end_color_idx = int((step + 1) * colors_per_step)
            avg_color = average_palette_slice(start_color_idx, end_color_idx)
            
            # Calculate the base x position for this step
            base_x_start = int((step / steps) * grad_width)
            base_x_end = int(((step + 1) / steps) * grad_width)
            
            # Apply wave displacement to each row
            for y in range(grad_height):
                # Calculate the wave offset for this row
                wave_offset = int(wave_shift[y] * grad_width)
                
                # Calculate the actual x positions for this row
                x_start = base_x_start + wave_offset
                x_end = base_x_end + wave_offset
                
                # Clamp to valid range
                x_start = max(0, min(grad_width - 1, x_start))
                x_end = max(0, min(grad_width, x_end))
                
                # Fill the band for this row
                if x_end > x_start:
                    gradient[y, x_start:x_end] = avg_color
    
    # Create final image with border
    border_rgb = hex_to_rgb(border_color) if border_color else hex_to_rgb(colors[0])
    img = Image.new('RGB', (width, height), border_rgb)
    img.paste(Image.fromarray(gradient), (border, border))
    
    return img


def generate_chunky_gradient(width: int, height: int, colors: List[str], steps: int,
                           orientation: str = 'horizontal', border: int = 0, border_color: str = None) -> Image.Image:
    """Generate a stepped gradient with discrete color bands."""
    grad_width = width - 2 * border
    grad_height = height - 2 * border
    
    if grad_width <= 0 or grad_height <= 0:
        raise ValueError("Border too large for image dimensions")
    
    # Helper to average a slice of the provided palette evenly per step
    def average_palette_slice(start_idx: int, end_idx: int) -> Tuple[int, int, int]:
        end_idx = max(start_idx + 1, end_idx)
        slice_colors = colors[start_idx:end_idx]
        rs = 0
        gs = 0
        bs = 0
        for color in slice_colors:
            r, g, b = hex_to_rgb(color)
            rs += r
            gs += g
            bs += b
        count = len(slice_colors)
        return (rs // count, gs // count, bs // count)
    
    # Calculate how many colors to average per step for even distribution
    colors_per_step = len(colors) / steps
    
    if orientation == 'horizontal':
        gradient = np.zeros((grad_height, grad_width, 3), dtype=np.uint8)
        step_width = grad_width // steps
        
        for step in range(steps):
            start_x = step * step_width
            end_x = (step + 1) * step_width if step < steps - 1 else grad_width
            
            # Calculate which slice of the palette to use for this step
            start_color_idx = int(step * colors_per_step)
            end_color_idx = int((step + 1) * colors_per_step)
            
            # Get the average color for this step
            avg_color = average_palette_slice(start_color_idx, end_color_idx)
            gradient[:, start_x:end_x] = avg_color
    else:  # vertical
        gradient = np.zeros((grad_height, grad_width, 3), dtype=np.uint8)
        step_height = grad_height // steps
        
        for step in range(steps):
            start_y = step * step_height
            end_y = (step + 1) * step_height if step < steps - 1 else grad_height
            
            # Calculate which slice of the palette to use for this step
            start_color_idx = int(step * colors_per_step)
            end_color_idx = int((step + 1) * colors_per_step)
            
            # Get the average color for this step
            avg_color = average_palette_slice(start_color_idx, end_color_idx)
            gradient[start_y:end_y, :] = avg_color
    
    # Create final image with border
    border_rgb = hex_to_rgb(border_color) if border_color else hex_to_rgb(colors[0])
    img = Image.new('RGB', (width, height), border_rgb)
    img.paste(Image.fromarray(gradient), (border, border))
    
    return img


def apply_grain(image: Image.Image, intensity: float = 0.1, mono: bool = False) -> Image.Image:
    """Apply uniform grain/noise to the image."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    if mono:
        # Monochromatic grain
        grain = np.random.normal(0, intensity * 255, (height, width, 3))
        grain = grain.astype(np.int16)
    else:
        # Color grain
        grain = np.random.normal(0, intensity * 255, (height, width, 3))
        grain = grain.astype(np.int16)
    
    # Apply grain
    result = img_array.astype(np.int16) + grain
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result)


def apply_grain_gradient(image: Image.Image, max_intensity: float = 0.3, min_intensity: float = 0.05, 
                        direction: str = 'vertical', mono: bool = False) -> Image.Image:
    """Apply grain with intensity that varies across the image."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    if direction == 'vertical':
        # Create intensity gradient from top to bottom
        intensity_gradient = np.linspace(min_intensity, max_intensity, height)
        intensity_gradient = intensity_gradient.reshape(-1, 1, 1)
    else:  # horizontal
        # Create intensity gradient from left to right
        intensity_gradient = np.linspace(min_intensity, max_intensity, width)
        intensity_gradient = intensity_gradient.reshape(1, -1, 1)
    
    if mono:
        # Monochromatic grain
        grain = np.random.normal(0, 1, (height, width, 3))
        grain = grain * intensity_gradient * 255
        grain = grain.astype(np.int16)
    else:
        # Color grain
        grain = np.random.normal(0, 1, (height, width, 3))
        grain = grain * intensity_gradient * 255
        grain = grain.astype(np.int16)
    
    # Apply grain
    result = img_array.astype(np.int16) + grain
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result)


def apply_grain_centered(image: Image.Image, max_intensity: float = 0.3, min_intensity: float = 0.05, 
                        mono: bool = False) -> Image.Image:
    """Apply grain with intensity that peaks in the center and fades towards edges."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    # Create distance from center
    y_center, x_center = height // 2, width // 2
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Calculate distance from center (normalized to 0-1)
    distance_from_center = np.sqrt(((y_coords - y_center) / y_center) ** 2 + 
                                   ((x_coords - x_center) / x_center) ** 2)
    
    # Create intensity map (strongest in center, fading to edges)
    intensity_map = max_intensity * (1 - distance_from_center)
    intensity_map = np.clip(intensity_map, min_intensity, max_intensity)
    intensity_map = intensity_map.reshape(height, width, 1)
    
    if mono:
        # Monochromatic grain
        grain = np.random.normal(0, 1, (height, width, 3))
        grain = grain * intensity_map * 255
        grain = grain.astype(np.int16)
    else:
        # Color grain
        grain = np.random.normal(0, 1, (height, width, 3))
        grain = grain * intensity_map * 255
        grain = grain.astype(np.int16)
    
    # Apply grain
    result = img_array.astype(np.int16) + grain
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result)


def apply_wave_rolling(image: Image.Image, wave_amplitude: float = 0.1, wave_frequency: float = 2.0) -> Image.Image:
    """Apply gentle rolling wave distortion to the image."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    # Create coordinate grids
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Normalize coordinates to 0-1
    y_norm = y_coords / height
    x_norm = x_coords / width
    
    # Create wave displacement
    wave_y = wave_amplitude * np.sin(2 * np.pi * wave_frequency * x_norm) * height
    wave_x = wave_amplitude * np.cos(2 * np.pi * wave_frequency * y_norm) * width * 0.3
    
    # Apply displacement
    new_y = (y_coords + wave_y).astype(np.int32)
    new_x = (x_coords + wave_x).astype(np.int32)
    
    # Clamp coordinates to valid range
    new_y = np.clip(new_y, 0, height - 1)
    new_x = np.clip(new_x, 0, width - 1)
    
    # Create new image with wave distortion
    result = img_array[new_y, new_x]
    
    return Image.fromarray(result)


def apply_wave_pooling(image: Image.Image, pool_strength: float = 0.3, pool_center_y: float = 0.6) -> Image.Image:
    """Apply dramatic central pooling effect like liquid gathering."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    # Create coordinate grids
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Normalize coordinates
    y_norm = y_coords / height
    x_norm = x_coords / width
    
    # Create pooling effect - stronger towards center and bottom
    center_x = 0.5
    center_y = pool_center_y
    
    # Distance from pool center
    dist_x = (x_norm - center_x) ** 2
    dist_y = (y_norm - center_y) ** 2
    distance = np.sqrt(dist_x + dist_y)
    
    # Pooling displacement (pulls pixels toward center)
    pool_factor = pool_strength * (1 - distance) * (1 - y_norm)  # Stronger at bottom
    pool_factor = np.clip(pool_factor, 0, 1)
    
    # Apply displacement
    displacement_x = (center_x - x_norm) * pool_factor * width * 0.5
    displacement_y = (center_y - y_norm) * pool_factor * height * 0.3
    
    new_x = (x_coords + displacement_x).astype(np.int32)
    new_y = (y_coords + displacement_y).astype(np.int32)
    
    # Clamp coordinates
    new_x = np.clip(new_x, 0, width - 1)
    new_y = np.clip(new_y, 0, height - 1)
    
    # Create new image
    result = img_array[new_y, new_x]
    
    return Image.fromarray(result)


def apply_wave_rippling(image: Image.Image, ripple_amplitude: float = 0.15, ripple_frequency: float = 3.0) -> Image.Image:
    """Apply rippling/undulating wave pattern."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    # Create coordinate grids
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Normalize coordinates
    y_norm = y_coords / height
    x_norm = x_coords / width
    
    # Create multiple overlapping ripples
    ripple1 = ripple_amplitude * np.sin(2 * np.pi * ripple_frequency * x_norm) * np.cos(2 * np.pi * ripple_frequency * y_norm)
    ripple2 = ripple_amplitude * 0.5 * np.sin(2 * np.pi * ripple_frequency * 1.5 * x_norm) * np.sin(2 * np.pi * ripple_frequency * 1.5 * y_norm)
    
    # Combine ripples
    total_ripple = ripple1 + ripple2
    
    # Apply displacement
    displacement_y = total_ripple * height
    displacement_x = total_ripple * width * 0.2
    
    new_y = (y_coords + displacement_y).astype(np.int32)
    new_x = (x_coords + displacement_x).astype(np.int32)
    
    # Clamp coordinates
    new_y = np.clip(new_y, 0, height - 1)
    new_x = np.clip(new_x, 0, width - 1)
    
    # Create new image
    result = img_array[new_y, new_x]
    
    return Image.fromarray(result)


def apply_wave_swirling(image: Image.Image, swirl_strength: float = 0.2, swirl_center_x: float = 0.5, swirl_center_y: float = 0.5) -> Image.Image:
    """Apply swirling/liquid flow effect."""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    # Create coordinate grids
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Normalize coordinates
    y_norm = y_coords / height
    x_norm = x_coords / width
    
    # Calculate distance and angle from swirl center
    center_x = swirl_center_x
    center_y = swirl_center_y
    
    dx = x_norm - center_x
    dy = y_norm - center_y
    distance = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    # Create swirling displacement
    swirl_factor = swirl_strength * (1 - distance)  # Stronger closer to center
    swirl_factor = np.clip(swirl_factor, 0, 1)
    
    # Apply rotation based on distance from center
    rotation_angle = swirl_factor * np.pi * 2  # Full rotation at center
    new_angle = angle + rotation_angle
    
    # Convert back to coordinates
    new_dx = distance * np.cos(new_angle)
    new_dy = distance * np.sin(new_angle)
    
    new_x = ((center_x + new_dx) * width).astype(np.int32)
    new_y = ((center_y + new_dy) * height).astype(np.int32)
    
    # Clamp coordinates
    new_x = np.clip(new_x, 0, width - 1)
    new_y = np.clip(new_y, 0, height - 1)
    
    # Create new image
    result = img_array[new_y, new_x]
    
    return Image.fromarray(result)


def analyze_gradient_colors(image_path: str, num_samples: int = 16) -> List[str]:
    """Extract a specified number of colors evenly from an image."""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        colors = []
        for i in range(num_samples):
            y = int((i + 0.5) * height / num_samples)
            x = int(width / 2)
            r, g, b = img_array[y, x]
            colors.append(rgb_to_hex((r, g, b)))
        
        return colors
    except Exception as e:
        print(f"Error analyzing image colors: {e}")
        return []


def extract_row_colors(image_path: str) -> List[str]:
    """Extract the average color from each row of an image."""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        colors = []
        for y in range(height):
            # Calculate average color for this row
            row_colors = img_array[y, :, :3]  # RGB channels only
            avg_r = int(np.mean(row_colors[:, 0]))
            avg_g = int(np.mean(row_colors[:, 1]))
            avg_b = int(np.mean(row_colors[:, 2]))
            colors.append(rgb_to_hex((avg_r, avg_g, avg_b)))
        
        return colors
    except Exception as e:
        print(f"Error extracting row colors: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description='Generate gradient images from hex colors')
    parser.add_argument('--mode', choices=['chunky', 'wave'], 
                       default='chunky', help='Gradient mode')
    parser.add_argument('--width', type=int, default=1000, help='Image width')
    parser.add_argument('--height', type=int, default=1000, help='Image height')
    parser.add_argument('--colors', nargs='+', help='Hex colors for gradient')
    parser.add_argument('--palette-file', help='File containing hex colors (one per line)')
    parser.add_argument('--steps', type=int, default=8, help='Number of steps for chunky mode')
    parser.add_argument('--orientation', choices=['horizontal', 'vertical'], 
                       default='horizontal', help='Gradient orientation')
    parser.add_argument('--border', type=int, default=0, help='Border width in pixels')
    parser.add_argument('--border-color', help='Border color in hex format')
    parser.add_argument('--output', default='gradient.png', help='Output filename')
    parser.add_argument('--grain', type=float, help='Grain intensity (0.0-1.0)')
    parser.add_argument('--grain-mono', action='store_true', help='Use monochromatic grain')
    parser.add_argument('--grain-gradient', nargs=2, type=float, metavar=('MAX', 'MIN'),
                       help='Grain with gradient intensity (max min)')
    parser.add_argument('--grain-direction', choices=['horizontal', 'vertical'], 
                       default='vertical', help='Direction for grain gradient')
    parser.add_argument('--grain-centered', nargs=2, type=float, metavar=('MAX', 'MIN'),
                       help='Grain with centered intensity (max min)')
    parser.add_argument('--wave-rolling', nargs=2, type=float, metavar=('AMPLITUDE', 'FREQUENCY'),
                       help='Apply rolling wave effect (amplitude frequency)')
    parser.add_argument('--wave-pooling', nargs=2, type=float, metavar=('STRENGTH', 'CENTER_Y'),
                       help='Apply pooling wave effect (strength center_y)')
    parser.add_argument('--wave-rippling', nargs=2, type=float, metavar=('AMPLITUDE', 'FREQUENCY'),
                       help='Apply rippling wave effect (amplitude frequency)')
    parser.add_argument('--wave-swirling', nargs=3, type=float, metavar=('STRENGTH', 'CENTER_X', 'CENTER_Y'),
                       help='Apply swirling wave effect (strength center_x center_y)')
    parser.add_argument('--wave-amplitude', type=float, default=0.3, help='Wave amplitude for wave mode (0.0-1.0)')
    parser.add_argument('--wave-frequency', type=float, default=2.0, help='Wave frequency for wave mode')
    parser.add_argument('--analyze', type=str, help='Analyze colors from image file')
    parser.add_argument('--extract-rows', type=str, help='Extract row colors from image file')
    
    args = parser.parse_args()
    
    # Get colors
    colors = []
    if args.colors:
        colors = args.colors
    elif args.palette_file:
        try:
            with open(args.palette_file, 'r') as f:
                colors = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: Palette file '{args.palette_file}' not found")
            return
    else:
        print("Error: Must provide either --colors or --palette-file")
        return
    
    if len(colors) < 2:
        print("Error: At least 2 colors are required for a gradient")
        return
    
    # Generate gradient
    if args.mode == 'wave':
        img = generate_wave_gradient(args.width, args.height, colors, args.steps,
                                   args.wave_amplitude, args.wave_frequency,
                                   args.orientation, args.border, args.border_color)
    else:  # chunky mode
        img = generate_chunky_gradient(args.width, args.height, colors, args.steps,
                                     args.orientation, args.border, args.border_color)
    
    # Apply grain if specified
    if args.grain:
        img = apply_grain(img, args.grain, args.grain_mono)
    elif args.grain_gradient:
        img = apply_grain_gradient(img, args.grain_gradient[0], args.grain_gradient[1], 
                                 args.grain_direction, args.grain_mono)
    elif args.grain_centered:
        img = apply_grain_centered(img, args.grain_centered[0], args.grain_centered[1], 
                                 args.grain_mono)
    
    # Apply wave effects if specified
    if args.wave_rolling:
        img = apply_wave_rolling(img, args.wave_rolling[0], args.wave_rolling[1])
    elif args.wave_pooling:
        img = apply_wave_pooling(img, args.wave_pooling[0], args.wave_pooling[1])
    elif args.wave_rippling:
        img = apply_wave_rippling(img, args.wave_rippling[0], args.wave_rippling[1])
    elif args.wave_swirling:
        img = apply_wave_swirling(img, args.wave_swirling[0], args.wave_swirling[1], args.wave_swirling[2])
    
    # Save image
    img.save(args.output)
    print(f"Gradient saved as '{args.output}'")
    
    # Handle analysis/extraction
    if args.analyze:
        colors = analyze_gradient_colors(args.analyze)
        if colors:
            print(f"Extracted {len(colors)} colors from '{args.analyze}':")
            for color in colors:
                print(color)
    
    if args.extract_rows:
        colors = extract_row_colors(args.extract_rows)
        if colors:
            print(f"Extracted {len(colors)} row colors from '{args.extract_rows}':")
            for color in colors:
                print(color)


if __name__ == '__main__':
    main()