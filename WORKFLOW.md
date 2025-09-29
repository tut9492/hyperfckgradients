# HyperfckGradients Workflow Guide

## 🎯 Standard Workflow

### 1. Extract Colors from Source Image
```bash
python3 src/ordered_gradient_extractor.py \
  --input examples/source_images/your_image.jpg \
  --num-colors 50 \
  --output data/palettes/extracted_palette.txt
```

### 2. Edit Palette (Optional)
- Open the generated palette file in any text editor
- Modify colors as needed
- Ensure one hex color per line

### 3. Generate Gradient
```bash
python3 src/gradient_generator.py \
  --mode wave \
  --palette-file data/palettes/extracted_palette.txt \
  --steps 50 \
  --width 2000 \
  --height 3000 \
  --border 100 \
  --border-color "#FFFFFF" \
  --wave-amplitude 0.2 \
  --wave-frequency 1.0 \
  --output examples/your_output.png
```

## 🎨 Quick Commands

### Purple Palette (Current Favorite)
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
  --output examples/purple_gradients/purple_50_bands.png
```

### Test Different Band Counts
```bash
# 10 bands
python3 src/gradient_generator.py --mode wave --palette-file data/palettes/purple_palette_new.txt --steps 10 --width 2000 --height 3000 --border 100 --border-color "#FFFFFF" --wave-amplitude 0.2 --wave-frequency 1.0 --output examples/purple_gradients/purple_10_bands.png

# 20 bands
python3 src/gradient_generator.py --mode wave --palette-file data/palettes/purple_palette_new.txt --steps 20 --width 2000 --height 3000 --border 100 --border-color "#FFFFFF" --wave-amplitude 0.2 --wave-frequency 1.0 --output examples/purple_gradients/purple_20_bands.png

# 30 bands
python3 src/gradient_generator.py --mode wave --palette-file data/palettes/purple_palette_new.txt --steps 30 --width 2000 --height 3000 --border 100 --border-color "#FFFFFF" --wave-amplitude 0.2 --wave-frequency 1.0 --output examples/purple_gradients/purple_30_bands.png

# 40 bands
python3 src/gradient_generator.py --mode wave --palette-file data/palettes/purple_palette_new.txt --steps 40 --width 2000 --height 3000 --border 100 --border-color "#FFFFFF" --wave-amplitude 0.2 --wave-frequency 1.0 --output examples/purple_gradients/purple_40_bands.png

# 50 bands
python3 src/gradient_generator.py --mode wave --palette-file data/palettes/purple_palette_new.txt --steps 50 --width 2000 --height 3000 --border 100 --border-color "#FFFFFF" --wave-amplitude 0.2 --wave-frequency 1.0 --output examples/purple_gradients/purple_50_bands.png
```

## 🔧 Parameter Tuning

### Wave Effects
- **Amplitude**: `0.1` (gentle) to `0.3` (dramatic)
- **Frequency**: `0.5` (slow waves) to `2.0` (fast waves)
- **Prime Settings**: `--wave-amplitude 0.2 --wave-frequency 1.0`

### Image Size
- **Standard**: `2000x3000` with `100px` border
- **Large**: `3000x4500` with `150px` border
- **Small**: `1000x1500` with `50px` border

### Band Count
- **Smooth**: 10-20 bands
- **Detailed**: 30-50 bands
- **Ultra-detailed**: 50+ bands

## 📁 File Organization

### Keep These Files
- `src/gradient_generator.py` - Main generator
- `src/ordered_gradient_extractor.py` - Color extraction
- `data/palettes/purple_palette_new.txt` - Current favorite palette
- `examples/purple_gradients/` - Your best outputs

### Archive These
- Old experimental palettes in `data/palettes/`
- Test images in `examples/experimental/`
- Source images in `examples/source_images/`

## 🎯 Best Practices

1. **Start with 50 bands** for maximum detail
2. **Use prime wave settings** for best results
3. **Keep source images organized** in `source_images/`
4. **Name outputs descriptively** (e.g., `purple_50_bands.png`)
5. **Test different band counts** to find your preference
6. **Edit palettes manually** for fine-tuning colors

## 🚀 Quick Start Template

```bash
# 1. Extract colors
python3 src/ordered_gradient_extractor.py --input your_image.jpg --num-colors 50 --output data/palettes/my_palette.txt

# 2. Generate gradient
python3 src/gradient_generator.py --mode wave --palette-file data/palettes/my_palette.txt --steps 50 --width 2000 --height 3000 --border 100 --border-color "#FFFFFF" --wave-amplitude 0.2 --wave-frequency 1.0 --output examples/my_gradient.png
```

That's it! Your gradient is ready. 🎨


