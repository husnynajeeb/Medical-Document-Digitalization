/**
 * Frontend Configuration
 * File: frontend/js/config.js
 */

const CONFIG = {
    // Backend API URL
    API_URL: 'http://localhost:8000',
    
    // File upload settings
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    ALLOWED_TYPES: ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff'],
    
    // Processing settings
    PROCESSING_STEPS: [
        'Enhancing image quality...',
        'Performing OCR...',
        'Correcting language...',
        'Generating corrected image...'
    ],
    
    // UI settings
    STEP_DELAY: 800, // Delay between processing step messages (ms)
    
    // Download settings
    ENHANCED_FILENAME: 'enhanced_document.png',
    CORRECTED_FILENAME: 'corrected_document.png'
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}