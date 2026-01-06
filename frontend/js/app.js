/**
 * Main Application Logic
 * File: frontend/js/app.js
 */

// Global state
let selectedFile = null;

// Feature flags
const FEATURES = {
  OCR_ENABLED: false, // Set to true when OCR is ready
  ENHANCEMENT_ENABLED: true,
};

// DOM elements
const fileInput = document.getElementById("fileInput");
const uploadSection = document.getElementById("uploadSection");
const previewSection = document.getElementById("previewSection");
const previewImage = document.getElementById("previewImage");
const processBtn = document.getElementById("processBtn");
const errorMessage = document.getElementById("errorMessage");
const processingOverlay = document.getElementById("processingOverlay");
const processingStatus = document.getElementById("processingStatus");
const resultsSection = document.getElementById("resultsSection");

// ============================================================================
// FILE UPLOAD HANDLING
// ============================================================================

fileInput.addEventListener("change", handleFileSelect);

function handleFileSelect(e) {
  const file = e.target.files[0];

  if (!file) return;

  // Validate file type
  if (!CONFIG.ALLOWED_TYPES.includes(file.type)) {
    showError("Please upload a valid image file (PNG, JPEG, BMP, or TIFF)");
    return;
  }

  // Validate file size
  if (file.size > CONFIG.MAX_FILE_SIZE) {
    showError(
      `File size must be less than ${CONFIG.MAX_FILE_SIZE / (1024 * 1024)}MB`
    );
    return;
  }

  selectedFile = file;

  // Preview the image
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewSection.classList.add("active");
    hideError();
  };
  reader.readAsDataURL(file);
}

// ============================================================================
// DRAG AND DROP
// ============================================================================

uploadSection.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadSection.classList.add("dragover");
});

uploadSection.addEventListener("dragleave", () => {
  uploadSection.classList.remove("dragover");
});

uploadSection.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadSection.classList.remove("dragover");

  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    handleFileSelect({ target: { files: [file] } });
  }
});

// ============================================================================
// DOCUMENT PROCESSING
// ============================================================================

processBtn.addEventListener("click", processDocument);

async function processDocument() {
  if (!selectedFile) {
    showError("Please select a file first");
    return;
  }

  // Show processing overlay
  showProcessing();
  processBtn.disabled = true;
  hideError();

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    // Update processing steps based on enabled features
    const steps = FEATURES.OCR_ENABLED
      ? CONFIG.PROCESSING_STEPS
      : ["Enhancing image quality..."];

    // Simulate processing steps
    for (let i = 0; i < steps.length; i++) {
      processingStatus.textContent = steps[i];
      if (i < steps.length - 1) {
        await delay(CONFIG.STEP_DELAY);
      }
    }

    // Send request to backend
    const response = await fetch(`${CONFIG.API_URL}/process`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Processing failed");
    }

    const result = await response.json();

    // DEBUG: Log the full response
    console.log("=== BACKEND RESPONSE ===");
    console.log("Full result:", JSON.stringify(result, null, 2));
    console.log("Processing time type:", typeof result.processing_time);
    console.log("Processing time value:", result.processing_time);
    console.log("Enhanced path:", result.enhanced_image_path);
    console.log("Success:", result.success);
    console.log("Message:", result.message);
    console.log("=======================");

    // Display results
    displayResults(result);
  } catch (error) {
    console.error("Error:", error);
    showError(
      `Error: ${error.message}. Make sure the backend server is running at ${CONFIG.API_URL}`
    );
  } finally {
    hideProcessing();
    processBtn.disabled = false;
  }
}

// ============================================================================
// RESULTS DISPLAY
// ============================================================================

function displayResults(result) {
  // Validate result object
  if (!result || typeof result !== "object") {
    showError("Invalid response from server");
    console.error("Invalid result object:", result);
    return;
  }

  console.log("Displaying results with OCR_ENABLED:", FEATURES.OCR_ENABLED);

  // Show results section
  resultsSection.style.display = "block";
  resultsSection.classList.add("active");

  try {
    if (FEATURES.OCR_ENABLED) {
      // Full results with OCR
      displayFullResults(result);
    } else {
      // Enhancement-only results
      displayEnhancementResults(result);
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    console.error("Error displaying results:", error);
    showError("Error displaying results: " + error.message);
  }
}

function displayEnhancementResults(result) {
  try {
    console.log("displayEnhancementResults called with:", result);

    // Hide OCR-related elements
    const ocrElements = document.querySelectorAll(".ocr-only");
    ocrElements.forEach((el) => (el.style.display = "none"));

    // Show only enhancement stats
    const statsCard = document.getElementById("statsCard");
    if (statsCard) {
      const processingTime = result.processing_time
        ? result.processing_time.toFixed(2)
        : "N/A";
      statsCard.innerHTML = `
                <h3>📊 Processing Stats</h3>
                <div class="stat-item">
                    <span class="stat-label">Processing Time:</span>
                    <span class="stat-value">${processingTime}s</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Status:</span>
                    <span class="stat-value">✓ Enhanced</span>
                </div>
                <div class="info-banner">
                    ℹ️ OCR is currently disabled. Only image enhancement is active.
                </div>
            `;
    } else {
      console.warn("statsCard element not found");
    }

    // Display enhanced image
    const enhancedImg = document.getElementById("enhancedImage");
    if (enhancedImg && result.enhanced_image_path) {
      const enhancedFilename = result.enhanced_image_path.split("/").pop();
      enhancedImg.src = `${CONFIG.API_URL}/download/enhanced/${enhancedFilename}`;
      console.log("Enhanced image set to:", enhancedImg.src);
    } else {
      console.warn("Enhanced image element or path not found");
    }

    // Hide corrected image section
    const correctedSection = document.getElementById("correctedImageSection");
    if (correctedSection) {
      correctedSection.style.display = "none";
    }

    // Hide text comparison sections
    const textSections = document.querySelectorAll(".text-comparison");
    textSections.forEach((section) => (section.style.display = "none"));

    // Setup download link for enhanced image only
    const downloadEnhanced = document.getElementById("downloadEnhanced");
    if (downloadEnhanced && enhancedImg && enhancedImg.src) {
      downloadEnhanced.href = enhancedImg.src;
      downloadEnhanced.download =
        CONFIG.ENHANCED_FILENAME || "enhanced_document.png";
    }

    // Hide corrected download button
    const downloadCorrected = document.getElementById("downloadCorrected");
    if (downloadCorrected) {
      downloadCorrected.style.display = "none";
    }

    console.log("displayEnhancementResults completed successfully");
  } catch (error) {
    console.error("Error in displayEnhancementResults:", error);
    throw error;
  }
}

function displayFullResults(result) {
  // Show all elements
  const ocrElements = document.querySelectorAll(".ocr-only");
  ocrElements.forEach((el) => (el.style.display = "block"));

  // Update stats with null checks
  const confidenceEl = document.getElementById("confidenceValue");
  const timeEl = document.getElementById("timeValue");
  const wordsEl = document.getElementById("wordsValue");

  if (confidenceEl && result.ocr_confidence != null) {
    confidenceEl.textContent = `${result.ocr_confidence.toFixed(1)}%`;
  }

  if (timeEl && result.processing_time != null) {
    timeEl.textContent = `${result.processing_time.toFixed(2)}s`;
  }

  if (wordsEl && result.original_text) {
    const wordCount = result.original_text
      .split(" ")
      .filter((w) => w.length > 0).length;
    wordsEl.textContent = wordCount;
  }

  // Display images
  const enhancedImg = document.getElementById("enhancedImage");
  const correctedImg = document.getElementById("correctedImage");

  if (result.enhanced_image_path) {
    const enhancedFilename = result.enhanced_image_path.split("/").pop();
    if (enhancedImg) {
      enhancedImg.src = `${CONFIG.API_URL}/download/enhanced/${enhancedFilename}`;
    }
  }

  if (result.corrected_image_path) {
    const correctedFilename = result.corrected_image_path.split("/").pop();
    if (correctedImg) {
      correctedImg.src = `${CONFIG.API_URL}/download/corrected/${correctedFilename}`;
    }
  }

  // Display text
  const originalTextEl = document.getElementById("originalText");
  const correctedTextEl = document.getElementById("correctedText");

  if (originalTextEl && result.original_text) {
    originalTextEl.textContent = result.original_text;
  }

  if (correctedTextEl && result.corrected_text) {
    correctedTextEl.textContent = result.corrected_text;
  }

  // Setup download links
  const downloadEnhanced = document.getElementById("downloadEnhanced");
  const downloadCorrected = document.getElementById("downloadCorrected");

  if (downloadEnhanced && enhancedImg && enhancedImg.src) {
    downloadEnhanced.href = enhancedImg.src;
    downloadEnhanced.download =
      CONFIG.ENHANCED_FILENAME || "enhanced_document.png";
  }

  if (downloadCorrected && correctedImg && correctedImg.src) {
    downloadCorrected.href = correctedImg.src;
    downloadCorrected.download =
      CONFIG.CORRECTED_FILENAME || "corrected_document.png";
  }
}

// ============================================================================
// UI HELPERS
// ============================================================================

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.classList.add("active");
}

function hideError() {
  errorMessage.classList.remove("active");
}

function showProcessing() {
  processingOverlay.classList.add("active");
}

function hideProcessing() {
  processingOverlay.classList.remove("active");
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("Medical Document Processor initialized");
  console.log("Backend URL:", CONFIG.API_URL);
  console.log("Features:", FEATURES);

  // Add feature status banner
  addFeatureBanner();

  // Check if backend is reachable
  checkBackendHealth();
});

function addFeatureBanner() {
  if (!FEATURES.OCR_ENABLED) {
    const banner = document.createElement("div");
    banner.className = "feature-banner";
    banner.innerHTML = `
            <strong>ℹ️ Development Mode:</strong> 
            OCR is currently disabled. Only image enhancement is active.
        `;
    banner.style.cssText = `
            background: #fef3c7;
            border: 2px solid #fbbf24;
            color: #92400e;
            padding: 12px 20px;
            margin: 20px auto;
            max-width: 1200px;
            border-radius: 8px;
            text-align: center;
            font-size: 14px;
        `;

    const container = document.querySelector(".container");
    if (container) {
      container.insertBefore(banner, container.firstChild);
    }
  }
}

async function checkBackendHealth() {
  try {
    const response = await fetch(`${CONFIG.API_URL}/health`);
    if (response.ok) {
      const health = await response.json();
      console.log("✓ Backend is healthy:", health);
      console.log("  - Enhancement enabled:", health.enhancement_enabled);
      console.log("  - OCR enabled:", health.ocr_enabled);

      // Sync frontend features with backend
      if (health.ocr_enabled !== FEATURES.OCR_ENABLED) {
        console.warn("⚠️ Frontend and backend OCR settings do not match!");
        console.warn(
          `  Frontend: ${FEATURES.OCR_ENABLED}, Backend: ${health.ocr_enabled}`
        );
      }
    } else {
      console.warn("⚠ Backend returned non-OK status");
    }
  } catch (error) {
    console.warn("⚠ Could not reach backend:", error.message);
    console.log("Make sure backend is running at:", CONFIG.API_URL);
  }
}
