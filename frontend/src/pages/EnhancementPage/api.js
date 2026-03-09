/**
 * Image Enhancement — API helpers (IT22348098)
 * All calls go to the /api/enhance* backend endpoints.
 */

const API_BASE = "http://localhost:8000";

/**
 * Enhance a single image file.
 * @param {File} file
 * @returns {Promise<{filename, original_image, enhanced_image, psnr, ssim, processing_time, status}>}
 */
export async function enhanceImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/enhancement/api/enhance`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "Enhancement failed" }));
    throw new Error(error.detail || "Enhancement failed");
  }

  return response.json();
}

/**
 * Enhance multiple image files in a single request.
 * @param {File[]} files
 * @returns {Promise<{results: Array, total: number}>}
 */
export async function enhanceBatch(files) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  const response = await fetch(`${API_BASE}/enhancement/api/enhance/batch`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "Batch enhancement failed" }));
    throw new Error(error.detail || "Batch enhancement failed");
  }

  return response.json();
}

/**
 * Health check — confirms backend is running and model is loaded.
 * @returns {Promise<{status, model_loaded, model_params}>}
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE}/enhancement/api/health`);
  return response.json();
}
