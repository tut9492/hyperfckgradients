#!/usr/bin/env python3
"""
Comprehensive Wave Generator

Generates all 16 wave variations (1A-1D, 2A-2D, 3A-3H) with vertical flipping support.
"""

import argparse
from typing import List, Tuple
from PIL import Image
import numpy as np
import math
import json
import os
import random


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_wave_variation(width: int, height: int, colors: List[str], steps: int,
                          wave_type: str, border: int = 0, border_color: str = None, 
                          wave_amplitude: float = 0.2, amplitude_scale: float = 1.0,
                          center_shift: float = 0.0, asymmetry: float = 0.0,
                          organic_jitter: float = 0.0, random_seed: int = None) -> Image.Image:
    """Generate a specific wave variation (1A-1D, 2A-2D, 3A-3H)."""
    grad_width = width - 2 * border
    grad_height = height - 2 * border
    
    if grad_width <= 0 or grad_height <= 0:
        raise ValueError("Border too large for image dimensions")
    
    # Helper to average a slice of the provided palette evenly per step
    def average_palette_slice(start_idx: int, end_idx: int) -> Tuple[int, int, int]:
        end_idx = max(start_idx + 1, end_idx)
        slice_colors = colors[start_idx:end_idx]
        if not slice_colors:
            return hex_to_rgb(colors[0])  # Fallback to first color
        rs = 0
        gs = 0
        bs = 0
        for color in slice_colors:
            r, g, b = hex_to_rgb(color)
            rs += r
            gs += g
            bs += b
        return (rs // len(slice_colors), gs // len(slice_colors), bs // len(slice_colors))
    
    # Calculate colors per step
    colors_per_step = len(colors) / steps
    
    # Create gradient array
    gradient = np.zeros((grad_height, grad_width, 3), dtype=np.uint8)

    # Prepare organic jitter (smooth noise across x) if requested
    smooth_noise = None
    if organic_jitter and organic_jitter != 0.0 and grad_width > 1:
        if random_seed is not None:
            np.random.seed(int(random_seed))
            random.seed(int(random_seed))
        x_coords = np.arange(grad_width)
        # Choose knot spacing ~80px, at least 2 knots
        n_knots = max(2, grad_width // 80)
        knot_positions = np.linspace(0, grad_width - 1, n_knots)
        knot_values = np.random.uniform(-1.0, 1.0, size=n_knots)
        # Interpolate to full width
        smooth_noise = np.interp(x_coords, knot_positions, knot_values)
        # Light smoothing
        kernel = np.array([0.25, 0.5, 0.25])
        smooth_noise = np.convolve(smooth_noise, kernel, mode='same')
    
    # Fill the gradient based on wave type
    for x in range(grad_width):
        for y in range(grad_height):
            # Normalize x position (0 to 1) for horizontal progression
            normalized_x = x / grad_width
            # Apply center shift (positive shifts center to the right)
            shifted_x = min(1.0, max(0.0, normalized_x - center_shift))
            
            # Determine wave parameters based on type
            current_amp = 0.0
            if wave_type == '0.0':  # Straight gradient (no waves)
                current_amp = 0.0
                wave_frequency = 1.0
            elif wave_type == '4A':  # Prime wave (bell curve intensity)
                # Calculate distance from center (0 at center, 1 at edges)
                center_distance = abs(shifted_x - 0.5) * 2
                # Create bell curve intensity (1 at center, 0 at edges)
                wave_intensity = (1 - center_distance) ** 2
                # Apply asymmetry exponent: >0 emphasizes left, <0 emphasizes right
                if asymmetry != 0.0:
                    if shifted_x < 0.5:
                        p = 1.0 + abs(asymmetry)
                        wave_intensity = wave_intensity ** p
                    else:
                        p = 1.0 + abs(asymmetry) if asymmetry < 0 else 1.0
                        wave_intensity = wave_intensity ** p
                current_amp = wave_amplitude * wave_intensity  # Prime wave amplitude
                wave_frequency = 1.0  # Single wave cycle
            elif wave_type == '4B':  # Inverted prime wave (valley curve intensity)
                # Calculate distance from center (0 at center, 1 at edges)
                center_distance = abs(shifted_x - 0.5) * 2
                # Create inverted bell curve intensity (0 at center, 1 at edges)
                wave_intensity = center_distance ** 2
                if asymmetry != 0.0:
                    if shifted_x < 0.5:
                        p = 1.0 + abs(asymmetry)
                        wave_intensity = wave_intensity ** p
                    else:
                        p = 1.0 + abs(asymmetry) if asymmetry < 0 else 1.0
                        wave_intensity = wave_intensity ** p
                current_amp = wave_amplitude * wave_intensity  # Inverted prime wave amplitude
                wave_frequency = 1.0  # Single wave cycle
            elif wave_type in ['1A', '1C']:  # Wave on left, straight on right
                if normalized_x < 0.3:  # Left 30%: wave
                    progress = normalized_x / 0.3
                    current_amp = (0.25 * amplitude_scale) * (1 - progress)
                else:  # Right 70%: flat
                    current_amp = 0.0
                wave_frequency = 1.5
                
            elif wave_type in ['1B', '1D']:  # Straight on left, wave on right
                if normalized_x > 0.7:  # Right 30%: wave
                    progress = (normalized_x - 0.7) / 0.3
                    current_amp = (0.25 * amplitude_scale) * progress
                else:  # Left 70%: flat
                    current_amp = 0.0
                wave_frequency = 1.5
                
            elif wave_type in ['2A', '2C']:  # 50/50 transition
                if normalized_x < 0.5:  # Left 50%: flat
                    current_amp = 0.0
                else:  # Right 50%: wave
                    progress = (normalized_x - 0.5) / 0.5
                    current_amp = (0.2 * amplitude_scale) * progress
                wave_frequency = 1.0
                
            elif wave_type in ['2B', '2D']:  # 50/50 transition flipped
                if normalized_x > 0.5:  # Right 50%: flat
                    current_amp = 0.0
                else:  # Left 50%: wave
                    progress = normalized_x / 0.5
                    current_amp = (0.2 * amplitude_scale) * (1 - progress)
                wave_frequency = 1.0

            elif wave_type == '2E':  # Single 2B-style wave shifted to center (0.25-0.75)
                if normalized_x < 0.25 or normalized_x > 0.75:
                    current_amp = 0.0  # Flat edges
                else:
                    # Map [0.25, 0.75] -> progress [0, 1]
                    progress = (normalized_x - 0.25) / 0.5
                    # Same shape as 2B: max at left of region, decays to 0 at right of region
                    current_amp = (0.2 * amplitude_scale) * (1 - progress)
                wave_frequency = 1.0
                
            else:  # Combined waves (3A-3B)
                if normalized_x < 0.5:  # Left half
                    if wave_type == '3A':  # Left half uses 1A (30% wave, 70% straight)
                        if normalized_x < 0.3:  # Left 30%: wave
                            progress = normalized_x / 0.3
                            current_amp = (0.25 * amplitude_scale) * (1 - progress)
                        else:  # Right 70%: flat
                            current_amp = 0.0
                        wave_frequency = 1.5
                    elif wave_type == '3B':  # Left half uses 1C (30% wave, 70% straight)
                        if normalized_x < 0.3:  # Left 30%: wave
                            progress = normalized_x / 0.3
                            current_amp = (0.25 * amplitude_scale) * (1 - progress)
                        else:  # Right 70%: flat
                            current_amp = 0.0
                        wave_frequency = 1.5
                    elif wave_type == '3C':  # Left half uses 1C (30% wave, 70% straight)
                        if normalized_x < 0.3:  # Left 30%: wave
                            progress = normalized_x / 0.3
                            current_amp = (0.25 * amplitude_scale) * (1 - progress)
                        else:  # Right 70%: flat
                            current_amp = 0.0
                        wave_frequency = 1.5
                    elif wave_type == '3D':  # Left half uses 1D (70% straight, 30% wave)
                        if normalized_x > 0.7:  # Right 30%: wave
                            progress = (normalized_x - 0.7) / 0.3
                            current_amp = (0.25 * amplitude_scale) * progress
                        else:  # Left 70%: flat
                            current_amp = 0.0
                        wave_frequency = 1.5
                else:  # Right half
                    if wave_type == '3A':  # Right half uses 2A (50% straight, 50% wave)
                        if normalized_x < 0.5:  # Left 50%: flat
                            current_amp = 0.0
                        else:  # Right 50%: wave
                            progress = (normalized_x - 0.5) / 0.5
                            current_amp = (0.2 * amplitude_scale) * progress
                        wave_frequency = 1.0
                    elif wave_type == '3B':  # Right half uses 2C (50% straight, 50% wave)
                        if normalized_x < 0.5:  # Left 50%: flat
                            current_amp = 0.0
                        else:  # Right 50%: wave
                            progress = (normalized_x - 0.5) / 0.5
                            current_amp = (0.2 * amplitude_scale) * progress
                        wave_frequency = 1.0
                    elif wave_type == '3C':  # Right half uses 2C (50% straight, 50% wave)
                        if normalized_x < 0.5:  # Left 50%: flat
                            current_amp = 0.0
                        else:  # Right 50%: wave
                            progress = (normalized_x - 0.5) / 0.5
                            current_amp = (0.2 * amplitude_scale) * progress
                        wave_frequency = 1.0
                    elif wave_type == '3D':  # Right half uses 2D (50% wave, 50% straight)
                        if normalized_x > 0.5:  # Right 50%: flat
                            current_amp = 0.0
                        else:  # Left 50%: wave
                            progress = normalized_x / 0.5
                            current_amp = (0.2 * amplitude_scale) * (1 - progress)
                        wave_frequency = 1.0
            
            # Calculate wave offset
            wave_offset = int(current_amp * grad_height * math.sin(2 * math.pi * wave_frequency * normalized_x))
            # Add organic jitter component if enabled
            if smooth_noise is not None:
                wave_offset += int(organic_jitter * grad_height * smooth_noise[x])
            
            # Apply vertical flip if needed
            if wave_type in ['1C', '1D', '2C', '2D', '3B', '3D']:
                adjusted_y = y - wave_offset  # Flip vertically
            else:
                adjusted_y = y + wave_offset
            
            # Determine which step this pixel should belong to
            step_y = adjusted_y / grad_height
            step = int(step_y * steps)
            step = max(0, min(steps - 1, step))
            
            # Get the color for this step
            start_color_idx = int(step * colors_per_step)
            end_color_idx = int((step + 1) * colors_per_step)
            avg_color = average_palette_slice(start_color_idx, end_color_idx)
            
            gradient[y, x] = avg_color
    
    # Fill any remaining black areas with the top band color (first color)
    top_color = hex_to_rgb(colors[0])
    for x in range(grad_width):
        for y in range(grad_height):
            if np.all(gradient[y, x] == 0):  # If pixel is black (unfilled)
                gradient[y, x] = top_color
    
    # Create final image with border
    if border > 0 and border_color:
        final_image = Image.new('RGB', (width, height), hex_to_rgb(border_color))
        grad_img = Image.fromarray(gradient)
        final_image.paste(grad_img, (border, border))
        return final_image
    else:
        return Image.fromarray(gradient)


def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive wave variations')
    parser.add_argument('--palette-file', required=True, help='Path to palette file')
    parser.add_argument('--steps', type=int, default=20, help='Number of gradient steps')
    parser.add_argument('--width', type=int, default=2000, help='Image width')
    parser.add_argument('--height', type=int, default=3000, help='Image height')
    parser.add_argument('--border', type=int, default=100, help='Border size')
    parser.add_argument('--border-color', default='#FFFFFF', help='Border color')
    parser.add_argument('--wave-amplitude', type=float, default=0.2, help='Wave amplitude (0.0 to 1.0)')
    parser.add_argument('--amplitude-scale', type=float, default=1.0, help='Scale factor for legacy wave families (1x/2x/3x)')
    parser.add_argument('--center-shift', type=float, default=0.0, help='Shift the wave center horizontally (-0.5 to 0.5)')
    parser.add_argument('--asymmetry', type=float, default=0.0, help='Asymmetry exponent control; positive favors left, negative favors right')
    parser.add_argument('--organic-jitter', type=float, default=0.0, help='Organic jitter amount (0.0-0.1 typical)')
    parser.add_argument('--random-seed', type=int, help='Seed for reproducible organic jitter')
    parser.add_argument('--wave-type', required=False, 
                       choices=['0.0', '1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', 
                               '3A', '3B', '3C', '3D', '4A', '4B'],
                       help='Wave variation type')
    parser.add_argument('--preset', type=str, help='Preset name from presets/wave_styles.json')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    # Apply preset if provided (preset supplies defaults; explicit flags override)
    if args.preset:
        presets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'presets', 'wave_styles.json')
        try:
            with open(presets_path, 'r') as pf:
                presets = json.load(pf)
            if args.preset not in presets:
                raise KeyError
            preset = presets[args.preset]
            # Only apply to fields that user left at parser defaults or unset
            if not args.wave_type and 'wave_type' in preset:
                args.wave_type = preset['wave_type']
            if args.wave_amplitude == 0.2 and 'wave_amplitude' in preset:
                args.wave_amplitude = float(preset['wave_amplitude'])
            if args.amplitude_scale == 1.0 and 'amplitude_scale' in preset:
                args.amplitude_scale = float(preset['amplitude_scale'])
            if args.steps == 20 and 'steps' in preset:
                args.steps = int(preset['steps'])
            if args.border == 100 and 'border' in preset:
                args.border = int(preset['border'])
            if args.border_color == '#FFFFFF' and 'border_color' in preset:
                args.border_color = str(preset['border_color'])
            if args.center_shift == 0.0 and 'center_shift' in preset:
                args.center_shift = float(preset['center_shift'])
            if args.asymmetry == 0.0 and 'asymmetry' in preset:
                args.asymmetry = float(preset['asymmetry'])
            if args.organic_jitter == 0.0 and 'organic_jitter' in preset:
                args.organic_jitter = float(preset['organic_jitter'])
            if args.random_seed is None and 'random_seed' in preset:
                args.random_seed = int(preset['random_seed'])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            raise SystemExit(f"Preset '{args.preset}' not found or presets file invalid.")

    if not args.wave_type:
        raise SystemExit("--wave-type is required unless a preset supplies it.")

    # Read palette - include colors that start with #
    with open(args.palette_file, 'r') as f:
        colors = [line.strip() for line in f if line.strip() and line.strip().startswith('#')]
    
    print(f"Loaded {len(colors)} colors: {colors[:3]}...")
    print(f"Generating Wave {args.wave_type} with {args.steps} bands")
    
    # Generate gradient
    gradient = generate_wave_variation(
        args.width, args.height, colors, args.steps,
        args.wave_type, args.border, args.border_color, args.wave_amplitude, args.amplitude_scale,
        args.center_shift, args.asymmetry, args.organic_jitter, args.random_seed
    )
    
    # Save image
    gradient.save(args.output)
    print(f"Wave {args.wave_type} gradient saved as '{args.output}'")


if __name__ == '__main__':
    main()
