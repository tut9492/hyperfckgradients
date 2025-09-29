#!/usr/bin/env python3
"""
HyperfckGradients - Main Entry Point
A modular gradient generator with wave effects and color extraction.
"""

import argparse
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gradient_generator import main as gradient_main
from color_extractor import main as extractor_main
from palette_expander import main as expander_main

def main():
    parser = argparse.ArgumentParser(
        description='HyperfckGradients - Advanced Gradient Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a gradient
  python main.py gradient --mode wave --palette-file data/palettes/purple_palette.txt --steps 50

  # Extract colors from an image
  python main.py extract --image input.png --num-colors 50 --output data/palettes/extracted.txt

  # Expand a palette
  python main.py expand --palette-file data/palettes/purple_palette.txt --num-colors 50
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Gradient generation subcommand
    gradient_parser = subparsers.add_parser('gradient', help='Generate gradients')
    gradient_parser.add_argument('--mode', choices=['straight-wave', 'progressive-wave', 'combined-wave'], default='straight-wave', help='Gradient mode')
    gradient_parser.add_argument('--palette-file', required=True, help='Palette file path')
    gradient_parser.add_argument('--steps', type=int, default=50, help='Number of gradient steps')
    gradient_parser.add_argument('--width', type=int, default=2000, help='Image width')
    gradient_parser.add_argument('--height', type=int, default=3000, help='Image height')
    gradient_parser.add_argument('--border', type=int, default=100, help='Border width')
    gradient_parser.add_argument('--border-color', default='#FFFFFF', help='Border color')
    gradient_parser.add_argument('--orientation', choices=['horizontal', 'horizontal-flipped'], 
                       default='horizontal', help='Gradient orientation')
    gradient_parser.add_argument('--wave-amplitude', type=float, default=0.08, help='Wave amplitude')
    gradient_parser.add_argument('--wave-frequency', type=float, default=2.5, help='Wave frequency')
    gradient_parser.add_argument('--grain-centered', nargs=2, type=float, metavar=('INTENSITY', 'SIZE'), help='Grain effect')
    gradient_parser.add_argument('--output', required=True, help='Output image file')
    
    # Color extraction subcommand
    extract_parser = subparsers.add_parser('extract', help='Extract colors from image')
    extract_parser.add_argument('--image', required=True, help='Input image file')
    extract_parser.add_argument('--num-colors', type=int, default=50, help='Number of colors to extract')
    extract_parser.add_argument('--output', help='Output palette file')
    
    # Palette expansion subcommand
    expand_parser = subparsers.add_parser('expand', help='Expand color palette')
    expand_parser.add_argument('--palette-file', required=True, help='Input palette file')
    expand_parser.add_argument('--num-colors', type=int, default=50, help='Target number of colors')
    expand_parser.add_argument('--output', help='Output palette file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to appropriate module
    if args.command == 'gradient':
        # Convert args to format expected by gradient_generator
        sys.argv = ['gradient_generator.py']
        for key, value in vars(args).items():
            if key != 'command' and value is not None:
                # Convert underscores to hyphens for gradient_generator arguments
                arg_name = key.replace('_', '-')
                if isinstance(value, bool):
                    if value:
                        sys.argv.append(f'--{arg_name}')
                elif isinstance(value, list):
                    sys.argv.extend([f'--{arg_name}'] + [str(v) for v in value])
                else:
                    sys.argv.extend([f'--{arg_name}', str(value)])
        gradient_main()
    
    elif args.command == 'extract':
        sys.argv = ['color_extractor.py']
        for key, value in vars(args).items():
            if key != 'command' and value is not None:
                sys.argv.extend([f'--{key}', str(value)])
        extractor_main()
    
    elif args.command == 'expand':
        sys.argv = ['palette_expander.py']
        for key, value in vars(args).items():
            if key != 'command' and value is not None:
                sys.argv.extend([f'--{key}', str(value)])
        expander_main()

if __name__ == '__main__':
    main()
