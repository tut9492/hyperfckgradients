// HyperfckGradients Dark Theme Interface JavaScript

class HyperfckGradientsApp {
    constructor() {
        this.currentImage = null;
        this.gallery = [];
        this.currentPanel = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadGallery();
    }

    setupEventListeners() {
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.generateWave();
        });

        document.getElementById('random-btn').addEventListener('click', () => {
            this.generateRandomWave();
        });

        // Modal functionality
        const modal = document.getElementById('imageModal');
        const modalImage = document.getElementById('modalImage');
        const modalClose = document.querySelector('.modal-close');

        // Click on preview image to open modal
        document.addEventListener('click', (e) => {
            if (e.target.id === 'preview-image') {
                this.openModal(e.target.src);
            }
        });

        // Close modal
        modalClose.addEventListener('click', () => {
            this.closeModal();
        });

        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Load gallery on page load
        document.addEventListener('DOMContentLoaded', () => {
            this.loadGallery();
        });
    }

    async generateWave() {
        const waveType = document.getElementById('wave-type').value;
        const palette = document.getElementById('palette').value;
        const grainEffect = document.getElementById('grain-effect').value;
        const bands = document.getElementById('bands').value;

        this.showLoading();

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wave_type: waveType,
                    palette: palette,
                    grain_effect: grainEffect,
                    bands: parseInt(bands)
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayImage(result.image_url, result.parameters);
                this.loadGallery(); // Refresh gallery
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Failed to generate wave: ' + error.message);
        }
    }

    async generateRandomWave() {
        this.showLoading();

        try {
            const response = await fetch('/generate_random', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();

            if (result.success) {
                this.displayImage(result.image_url, result.parameters);
                this.loadGallery(); // Refresh gallery
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Failed to generate random wave: ' + error.message);
        }
    }

    displayImage(imageUrl, parameters) {
        const previewImage = document.getElementById('preview-image');
        const previewPlaceholder = document.getElementById('preview-placeholder');
        const loading = document.getElementById('loading');

        // Hide loading and placeholder
        loading.style.display = 'none';
        previewPlaceholder.style.display = 'none';

        // Show image
        previewImage.src = imageUrl;
        previewImage.style.display = 'block';

        // Store current image info
        this.currentImage = {
            url: imageUrl,
            parameters: parameters
        };
    }

    showLoading() {
        const loading = document.getElementById('loading');
        const previewImage = document.getElementById('preview-image');
        const previewPlaceholder = document.getElementById('preview-placeholder');

        loading.style.display = 'block';
        previewImage.style.display = 'none';
        previewPlaceholder.style.display = 'none';
    }

    showError(message) {
        const loading = document.getElementById('loading');
        const previewPlaceholder = document.getElementById('preview-placeholder');

        loading.style.display = 'none';
        previewPlaceholder.style.display = 'block';
        previewPlaceholder.innerHTML = `<p style="color: #ff6b6b;">Error: ${message}</p>`;
    }

    async loadGallery() {
        try {
            const response = await fetch('/gallery');
            const gallery = await response.json();

            this.gallery = gallery;
            this.displayGallery();
        } catch (error) {
            console.error('Failed to load gallery:', error);
        }
    }

    displayGallery() {
        const galleryGrid = document.getElementById('gallery-grid');
        galleryGrid.innerHTML = '';

        this.gallery.forEach(item => {
            const galleryItem = document.createElement('div');
            galleryItem.className = 'gallery-item';
            
            // Extract parameters from filename
            const filename = item.filename;
            const parts = filename.split('_');
            const waveType = parts[1] || 'Unknown';
            const palette = parts[2] || 'Unknown';
            const grainEffect = parts[3] || 'none';
            
            galleryItem.innerHTML = `
                <img src="${item.image_url}" alt="Generated Wave" loading="lazy">
                <div class="gallery-item-info">
                    <div class="param">
                        <span class="param-label">Wave:</span>
                        <span class="param-value">${waveType}</span>
                    </div>
                    <div class="param">
                        <span class="param-label">Palette:</span>
                        <span class="param-value">${palette}</span>
                    </div>
                    <div class="param">
                        <span class="param-label">Grain:</span>
                        <span class="param-value">${grainEffect}</span>
                    </div>
                    <div class="param">
                        <span class="param-label">Created:</span>
                        <span class="param-value">${new Date(item.created).toLocaleDateString()}</span>
                    </div>
                </div>
            `;

            // Add click handler to regenerate from gallery item
            galleryItem.addEventListener('click', () => {
                this.regenerateFromGallery(item);
            });

            galleryGrid.appendChild(galleryItem);
        });
    }

    regenerateFromGallery(item) {
        // Extract parameters from filename if possible
        const filename = item.filename;
        const parts = filename.split('_');
        
        if (parts.length >= 3) {
            const waveType = parts[1];
            const palette = parts[2];
            const grainEffect = parts[3];

            // Set form values
            document.getElementById('wave-type').value = waveType;
            document.getElementById('palette').value = palette;
            document.getElementById('grain-effect').value = grainEffect;

            // Display the gallery image in the main preview
            this.displayImage(item.image_url, {
                wave_type: waveType,
                palette: palette,
                grain_effect: grainEffect
            });
        }
    }

    openModal(imageSrc) {
        const modal = document.getElementById('imageModal');
        const modalImage = document.getElementById('modalImage');
        
        modalImage.src = imageSrc;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    closeModal() {
        const modal = document.getElementById('imageModal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new HyperfckGradientsApp();
});