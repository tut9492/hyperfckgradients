# HyperfckGradients

A modular Python toolkit for generating advanced gradients with wave effects, color extraction, and palette manipulation.

## Features

- **Wave Gradients**: Create flowing, organic gradient patterns with customizable wave effects
- **Color Extraction**: Extract color palettes from existing images
- **Palette Expansion**: Interpolate between colors to create larger palettes
- **Modular Design**: Clean, reusable code structure
- **High Resolution**: Generate gradients up to 4K+ resolution

## Installation

```bash
git clone https://github.com/yourusername/HyperfckGradients.git
cd HyperfckGradients
pip install -r requirements.txt
```

## Quick Start

### Generate a Wave Gradient
```bash
python main.py gradient --mode wave --palette-file data/palettes/purple_palette.txt --steps 50 --output my_gradient.png
```

### Extract Colors from an Image
```bash
python main.py extract --image input.png --num-colors 50 --output data/palettes/extracted.txt
```

### Expand a Color Palette
```bash
python main.py expand --palette-file data/palettes/purple_palette.txt --num-colors 50 --output data/palettes/expanded.txt
```

## Project Structure

```
HyperfckGradients/
├── src/                    # Source code modules
│   ├── gradient_generator.py    # Main gradient generation
│   ├── color_extractor.py       # Color extraction from images
│   └── palette_expander.py      # Palette interpolation
├── data/
│   └── palettes/           # Color palette files
├── examples/               # Example outputs
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Usage Examples

### Basic Wave Gradient
```bash
python main.py gradient \
  --mode wave \
  --palette-file data/palettes/purple_palette.txt \
  --steps 16 \
  --width 2000 \
  --height 3000 \
  --border 100 \
  --border-color "#FFFFFF" \
  --wave-amplitude 0.08 \
  --wave-frequency 2.5 \
  --output purple_wave.png
```

### High-Resolution with Grain Effect
```bash
python main.py gradient \
  --mode wave \
  --palette-file data/palettes/greyscale_palette.txt \
  --steps 50 \
  --width 4000 \
  --height 6000 \
  --grain-centered 0.2 0.05 \
  --output high_res_grain.png
```

### Extract and Use Colors
```bash
# Extract colors from an image
python main.py extract --image source.png --num-colors 50 --output data/palettes/extracted.txt

# Use extracted colors for gradient
python main.py gradient --mode wave --palette-file data/palettes/extracted.txt --steps 50 --output reconstructed.png
```

## Parameters

### Gradient Generation
- `--mode`: `wave` or `chunky` gradient style
- `--palette-file`: Path to color palette file
- `--steps`: Number of gradient steps/bands
- `--width/--height`: Image dimensions
- `--border`: Border width in pixels
- `--border-color`: Border color (hex)
- `--wave-amplitude`: Wave strength (0.0-1.0)
- `--wave-frequency`: Wave frequency
- `--grain-centered`: Grain effect intensity and size

### Color Extraction
- `--image`: Source image file
- `--num-colors`: Number of colors to extract
- `--output`: Output palette file

### Palette Expansion
- `--palette-file`: Input palette file
- `--num-colors`: Target number of colors
- `--output`: Output palette file

## Color Palette Format

Palette files should contain one hex color per line:
```
#2D1B69
#4A2B8A
#6B3FA3
#8B5BB8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Examples

Check the `examples/` directory for sample outputs and use cases.
