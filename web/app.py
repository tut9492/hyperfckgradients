#!/usr/bin/env python3
"""
HyperfckGradients Web Interface
NFT-ready generative wave art interface
"""

import os
import sys
import json
import random
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import uuid
from datetime import datetime

# Add parent directory to path to import wave generators
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.comprehensive_wave_generator import generate_wave_variation
from src.grain_processor import apply_dithering_grain
from src.white_grain import apply_white_grain

app = Flask(__name__)

# Configuration
GENERATED_DIR = os.path.join(os.path.dirname(__file__), 'generated')
PALETTES_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'palettes')
PRESETS_FILE = os.path.join(os.path.dirname(__file__), '..', 'presets', 'wave_styles.json')

# Ensure directories exist
os.makedirs(GENERATED_DIR, exist_ok=True)

# Load available palettes
def load_palettes():
    """Load all palettes from Excel file."""
    # Define all palettes we want to use - Updated to include dotsmall and doftiny
    new_palettes = [
        'pink_to_black_to_cyan',
        'orange_to_teal', 
        'green_with_bar',
        'purple_to_orange',
        'magenta_to_blue',
        'rainbow_pastel',
        'purple_to_peach',
        'bluegray_to_lavender',
        'yellow_pink_green',
        'purple_to_teal',
        'purple',
        'pastel_rainbow',
        'red_to_brothko',
        'gradient_301',
        'gradient_298',
        'dotsmall',
        'doftiny',
        'user_provided_gradient',
              'test_palette_brown_25bands',
        'rectangle_306',
        'rectangle_305',
        'temp'
    ]
    
    palettes = {}
    if os.path.exists(PALETTES_DIR):
        for filename in os.listdir(PALETTES_DIR):
            if filename.endswith('.txt'):
                palette_name = filename.replace('.txt', '')
                # Only include the new palettes
                if palette_name in new_palettes:
                    # Create clean display names
                    clean_name = palette_name.replace('_', ' ').title()
                    palettes[palette_name] = {
                        'file_path': os.path.join(PALETTES_DIR, filename),
                        'display_name': clean_name
                    }
    return palettes

# Load presets
def load_presets():
    """Load wave style presets."""
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Available wave types
WAVE_TYPES = {
    '0.0': '0.0',
    '1A': '1A',
    '1B': '1B',
    '1C': '1C',
    '1D': '1D',
    '2A': '2A',
    '2B': '2B',
    '2C': '2C',
    '2D': '2D',
    '3A': '3A',
    '3B': '3B',
    '3C': '3C',
    '3D': '3D',
    '4A': '4A',
    '4B': '4B',
    '5A': '5A',
    '5B': '5B',
    '5C': '5C',
    '5D': '5D'
}

# Available grain effects
GRAIN_EFFECTS = {
    'none': 'No Grain',
    'dithering': 'Dithering',
    'white_grain': 'White Grain'
}

@app.route('/')
def index():
    """Main interface page."""
    palettes = load_palettes()
    return render_template('index.html', 
                         palettes=palettes, 
                         wave_types=WAVE_TYPES,
                         grain_effects=GRAIN_EFFECTS)

@app.route('/generate', methods=['POST'])
def generate_wave():
    """Generate a wave image with specified parameters."""
    try:
        data = request.json
        wave_type = data.get('wave_type', '4A')
        palette_name = data.get('palette', 'blue_to_yellow_50')
        grain_effect = data.get('grain_effect', 'none')
        bands = data.get('bands', 20)
        
        # Load palettes
        palettes = load_palettes()
        if palette_name not in palettes:
            return jsonify({'error': 'Palette not found'}), 400
        
        palette_file = palettes[palette_name]['file_path']
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"wave_{wave_type}_{palette_name}_{grain_effect}_{timestamp}_{unique_id}.png"
        output_path = os.path.join(GENERATED_DIR, filename)
        
        # Load palette colors
        with open(palette_file, 'r') as f:
            colors = [line.strip() for line in f if line.strip() and line.strip().startswith('#')]
        
        # Use default parameters for all wave types
        wave_amplitude = 0.2
        amplitude_scale = 1.0
        center_shift = 0.0
        asymmetry = 0.0
        organic_jitter = 0.0
        random_seed = None
        
        # Generate the wave
        wave_image = generate_wave_variation(
            width=2000, height=3000, colors=colors, steps=bands,
            wave_type=wave_type, border=100, border_color='#FFFFFF',
            wave_amplitude=wave_amplitude, amplitude_scale=amplitude_scale,
            center_shift=center_shift, asymmetry=asymmetry,
            organic_jitter=organic_jitter, random_seed=random_seed
        )
        
        # Apply grain effect if specified
        if grain_effect == 'dithering':
            wave_image = apply_dithering_grain(wave_image, intensity=0.15, grain_size=1.2, border_size=100)
        elif grain_effect == 'white_grain':
            wave_image = apply_white_grain(wave_image, base_intensity=0.01, density_variation=0.2, size_variation=0.3, border_size=100)
        
        # Save image
        wave_image.save(output_path)
        
        # Return success with image info
        return jsonify({
            'success': True,
            'filename': filename,
            'image_url': f'/generated/{filename}',
            'parameters': {
                'wave_type': wave_type,
                'palette': palette_name,
                'grain_effect': grain_effect,
                'bands': bands
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_random', methods=['POST'])
def generate_random_wave():
    """Generate a completely random wave for NFT generation."""
    try:
        # Random parameters
        wave_type = random.choice(list(WAVE_TYPES.keys()))
        palettes = load_palettes()
        palette_name = random.choice(list(palettes.keys()))
        grain_effect = random.choice(list(GRAIN_EFFECTS.keys()))
        
        # Random organic parameters for 4A/4B/5A-5D
        if wave_type in ['4A', '4B', '5A', '5B', '5C', '5D']:
            wave_amplitude = random.uniform(0.02, 0.3)
            center_shift = random.uniform(-0.2, 0.2)
            asymmetry = random.uniform(-1.0, 1.0)
            organic_jitter = random.uniform(0.0, 0.05)
            random_seed = random.randint(1, 1000000)
        else:
            wave_amplitude = random.uniform(0.1, 0.4)
            amplitude_scale = random.uniform(0.3, 1.5)
            center_shift = 0.0
            asymmetry = 0.0
            organic_jitter = 0.0
            random_seed = None
        
        # Generate with random parameters
        palette_file = palettes[palette_name]['file_path']
        with open(palette_file, 'r') as f:
            colors = [line.strip() for line in f if line.strip() and line.strip().startswith('#')]
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"random_{wave_type}_{palette_name}_{grain_effect}_{timestamp}_{unique_id}.png"
        output_path = os.path.join(GENERATED_DIR, filename)
        
        # Generate the wave
        wave_image = generate_wave_variation(
            width=2000, height=3000, colors=colors, steps=20,
            wave_type=wave_type, border=100, border_color='#FFFFFF',
            wave_amplitude=wave_amplitude, amplitude_scale=amplitude_scale,
            center_shift=center_shift, asymmetry=asymmetry,
            organic_jitter=organic_jitter, random_seed=random_seed
        )
        
        # Apply grain effect with fixed settings
        if grain_effect == 'dithering':
            wave_image = apply_dithering_grain(wave_image, intensity=0.15, grain_size=1.2, border_size=100)
        elif grain_effect == 'white_grain':
            wave_image = apply_white_grain(wave_image, base_intensity=0.01, density_variation=0.2, size_variation=0.3, border_size=100)
        
        # Save image
        wave_image.save(output_path)
        
        # Return success with random parameters
        return jsonify({
            'success': True,
            'filename': filename,
            'image_url': f'/generated/{filename}',
            'parameters': {
                'wave_type': wave_type,
                'palette': palette_name,
                'grain_effect': grain_effect,
                'wave_amplitude': wave_amplitude,
                'center_shift': center_shift,
                'asymmetry': asymmetry,
                'organic_jitter': organic_jitter,
                'random_seed': random_seed
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generated/<filename>')
def serve_generated(filename):
    """Serve generated images."""
    return send_file(os.path.join(GENERATED_DIR, filename))

@app.route('/gallery')
def get_gallery():
    """Get list of generated images for gallery."""
    try:
        gallery_items = []
        if os.path.exists(GENERATED_DIR):
            for filename in os.listdir(GENERATED_DIR):
                if filename.endswith('.png'):
                    file_path = os.path.join(GENERATED_DIR, filename)
                    stat = os.stat(file_path)
                    gallery_items.append({
                        'filename': filename,
                        'image_url': f'/generated/{filename}',
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'size': stat.st_size
                    })
        
        # Sort by creation time (newest first)
        gallery_items.sort(key=lambda x: x['created'], reverse=True)
        return jsonify(gallery_items)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
