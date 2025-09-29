# HyperfckGradients

A powerful Python toolkit for generating beautiful gradient images with wave effects, color extraction, and palette management.

## 🎨 Features

- **Gradient Generation**: Create chunky and wave-effect gradients
- **Color Extraction**: Extract color palettes from images while preserving order
- **Palette Management**: Organize and expand color palettes
- **Wave Effects**: Apply sinusoidal wave distortions with customizable amplitude and frequency
- **Multiple Formats**: Support for various gradient orientations and border styles

## 📁 Project Structure

```
HyperfckGradients/
├── src/                          # Core modules
│   ├── gradient_generator.py     # Main gradient generation
│   ├── color_extractor.py        # Color extraction from images
│   ├── ordered_gradient_extractor.py  # Preserve gradient order
│   ├── palette_expander.py       # Expand color palettes
│   └── ...                       # Additional utilities
├── data/
│   └── palettes/                 # Color palette files
├── examples/                     # Generated gradient examples
│   ├── purple_gradients/         # Purple-themed gradients
│   ├── greyscale_gradients/      # Greyscale gradients
│   ├── source_images/            # Original source images
│   └── experimental/             # Experimental outputs
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Installation

```bash
git clone <repository-url>
cd HyperfckGradients
pip install -r requirements.txt
```

### Basic Usage

#### Generate a Wave Gradient

```bash
python3 src/gradient_generator.py \
  --mode wave \
  --palette-file data/palettes/purple_palette_new.txt \
  --steps 50 \
  --width 2000 \
  --height 3000 \
  --border 100 \
  --border-color "#FFFFFF" \
  --wave-amplitude 0.2 \
  --wave-frequency 1.0 \
  --output examples/purple_gradients/my_gradient.png
```

#### Extract Colors from an Image

```bash
python3 src/ordered_gradient_extractor.py \
  --input examples/source_images/my_image.jpg \
  --num-colors 50 \
  --output data/palettes/extracted_palette.txt
```

#### Expand a Palette

```bash
python3 src/palette_expander.py \
  --input data/palettes/base_palette.txt \
  --output-size 50 \
  --output data/palettes/expanded_palette.txt
```

## 🎛️ Parameters

### Gradient Generator

- `--mode`: `chunky` or `wave`
- `--palette-file`: Path to color palette file
- `--steps`: Number of gradient bands
- `--width` / `--height`: Image dimensions
- `--border`: Border width in pixels
- `--border-color`: Border color (hex)
- `--wave-amplitude`: Wave intensity (0.0-1.0)
- `--wave-frequency`: Number of wave cycles
- `--orientation`: `horizontal` or `vertical`
- `--grain-centered`: Add grain effect (strength, size)

### Color Extractor

- `--input`: Source image path
- `--num-colors`: Number of colors to extract
- `--output`: Output palette file path
- `--orientation`: `horizontal` or `vertical` (for ordered extraction)

## 🎨 Palette Format

Color palettes are simple text files with one hex color per line:

```
#040208
#37276e
#47367f
#56458e
#6c5ba5
#8372bb
#f8f9fa
```

## 📊 Current Workflow

1. **Source Image**: Start with a reference image
2. **Color Extraction**: Use `ordered_gradient_extractor.py` to extract colors while preserving order
3. **Palette Refinement**: Edit the palette file to adjust colors
4. **Gradient Generation**: Use `gradient_generator.py` with wave effects
5. **Iteration**: Adjust parameters and regenerate as needed

## 🔧 Advanced Features

### Prime Wave Configuration

For optimal wave effects, use these parameters:
- `--wave-amplitude 0.2`
- `--wave-frequency 1.0`

### Gap Filling Logic

The wave generator includes intelligent gap-filling:
- Top half of gaps: First color from palette
- Bottom half of gaps: Last color from palette
- Ensures clean, solid fills in wave dips

### Color Order Preservation

The `ordered_gradient_extractor.py` maintains the original gradient flow by sampling colors sequentially from top-to-bottom (or left-to-right for horizontal gradients).

## 📝 Examples

Check the `examples/` directory for:
- **Purple Gradients**: Various purple-themed wave gradients
- **Greyscale Gradients**: Monochrome gradient examples
- **Source Images**: Original reference images
- **Experimental**: Testing and development outputs

## 🛠️ Development

### Adding New Features

1. Create new modules in `src/`
2. Update `main.py` for command-line integration
3. Add examples to `examples/experimental/`
4. Update this README

### Testing

```bash
# Test gradient generation
python3 src/gradient_generator.py --help

# Test color extraction
python3 src/ordered_gradient_extractor.py --help
```

## 📄 License

This project is open source. Feel free to use and modify as needed.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy Gradient Making!** 🎨✨