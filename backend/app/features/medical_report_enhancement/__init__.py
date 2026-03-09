"""
Medical Report Enhancement — IT22348098
========================================
U-Net model loader and patch-based inference engine for document
deblurring and denoising.
"""

import numpy as np

try:
    import tensorflow as tf

    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


class ModelEnhancer:
    """Load a Keras U-Net and run overlapping-patch inference on grayscale images."""

    def __init__(self, model_path: str, batch_size: int = 32):
        self.model = None
        self.is_loaded = False
        self.param_count = 0
        self.patch_size = 128
        self.batch_size = batch_size
        self._model_path = model_path

        if not TF_AVAILABLE:
            print("⚠️  TensorFlow not installed — model loading skipped")
            return

        self._load_model()

    def _load_model(self) -> None:
        """Load the Keras model from *self._model_path*."""
        print("  TensorFlow  installed — model loaded")
        try:
            custom_objects = {
                "document_loss": self._document_loss,
                "psnr_metric_fn": self._psnr_metric,
                "ssim_metric_fn": self._ssim_metric,
            }
            self.model = tf.keras.models.load_model(
                self._model_path, custom_objects=custom_objects
            )
            self.is_loaded = True
            self.param_count = self.model.count_params()
            print(f"✅ Model loaded: {self.param_count:,} parameters")
        except Exception as e:
            print(f"⚠️  Model not loaded: {e}")
            print("Place your best_model.keras in models/medical_report_enhancement/")

    def enhance(self, img_gray: np.ndarray):
        """
        Enhance a full-size grayscale image using patch-based inference.

        Returns: (enhanced_image, psnr, ssim)
        PSNR/SSIM are None since we have no ground truth in production.
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Model not loaded. "
                "Place best_model.keras in models/medical_report_enhancement/"
            )

        h, w = img_gray.shape
        img_norm = img_gray.astype(np.float32) / 255.0

        # Pad so both dimensions are divisible by patch_size
        pad_h = (self.patch_size - h % self.patch_size) % self.patch_size
        pad_w = (self.patch_size - w % self.patch_size) % self.patch_size
        img_padded = np.pad(img_norm, ((0, pad_h), (0, pad_w)), mode="reflect")

        h_pad, w_pad = img_padded.shape
        output = np.zeros_like(img_padded)
        count = np.zeros_like(img_padded)

        stride = self.patch_size // 2  # 50% overlap for smooth stitching

        patches = []
        positions = []
        for y in range(0, h_pad - self.patch_size + 1, stride):
            for x in range(0, w_pad - self.patch_size + 1, stride):
                patch = img_padded[y : y + self.patch_size, x : x + self.patch_size]
                patches.append(patch)
                positions.append((y, x))

        # Batch predict
        patches_array = np.array(patches)[..., np.newaxis]
        enhanced_patches = self.model.predict(patches_array, batch_size=self.batch_size, verbose=0)

        # Stitch back with averaging over overlapping regions
        for (y, x), ep in zip(positions, enhanced_patches):
            output[y : y + self.patch_size, x : x + self.patch_size] += ep[:, :, 0]
            count[y : y + self.patch_size, x : x + self.patch_size] += 1.0

        output = output / np.maximum(count, 1.0)
        output = output[:h, :w]  # Remove padding
        enhanced = np.clip(output * 255, 0, 255).astype(np.uint8)

        return enhanced, None, None

    # ── Custom Keras loss / metrics ────────────────────────────────────────────

    @staticmethod
    def _document_loss(y_true, y_pred):
        """Text-optimised composite loss: 0.5×L1 + 0.3×SSIM + 0.2×Edge."""
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.cast(y_pred, tf.float32)
        l1 = tf.reduce_mean(tf.abs(y_true - y_pred))
        ssim_val = 1.0 - tf.reduce_mean(
            tf.image.ssim(y_true, y_pred, max_val=1.0)
        )
        true_edges = tf.image.sobel_edges(y_true)
        pred_edges = tf.image.sobel_edges(y_pred)
        edge_loss = tf.reduce_mean(tf.abs(true_edges - pred_edges))
        return 0.5 * l1 + 0.3 * ssim_val + 0.2 * edge_loss

    @staticmethod
    def _psnr_metric(y_true, y_pred):
        return tf.reduce_mean(
            tf.image.psnr(
                tf.cast(y_true, tf.float32),
                tf.cast(y_pred, tf.float32),
                max_val=1.0,
            )
        )

    @staticmethod
    def _ssim_metric(y_true, y_pred):
        return tf.reduce_mean(
            tf.image.ssim(
                tf.cast(y_true, tf.float32),
                tf.cast(y_pred, tf.float32),
                max_val=1.0,
            )
        )
