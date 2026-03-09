/**
 * Enhancement Page — IT22348098
 * --------------------------------
 * Medical Report Image Enhancement feature page.
 * Self-contained: manages its own state, toast notifications, and all UI.
 * No header — drop it into any layout your teammates build.
 *
 * Usage:
 *   import EnhancementPage from './pages/EnhancementPage';
 *   <EnhancementPage />
 */

import { useState, useCallback } from 'react';

import UploadZone from './components/UploadZone.jsx';
import ImageGallery from './components/ImageGallery.jsx';
import Lightbox from './components/Lightbox.jsx';
import { enhanceBatch } from './api.js';
import './EnhancementPage.css';

function EnhancementPage() {
  const [images, setImages] = useState([]);
  const [selectedImageId, setSelectedImageId] = useState(null);
  const [lightbox, setLightbox] = useState(null); // { url, type, imageId }
  const [isProcessing, setIsProcessing] = useState(false);
  const [toast, setToast] = useState(null); // { message, type: 'success'|'error' }

  // ── Toast ───────────────────────────────────────────────────────────────────
  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  }, []);

  // ── File selection ──────────────────────────────────────────────────────────
  const handleFilesSelected = useCallback((files) => {
    const newImages = files.map((file) => ({
      id: crypto.randomUUID(),
      file,
      originalUrl: URL.createObjectURL(file),
      enhancedUrl: null,
      status: 'pending',
      psnr: null,
      ssim: null,
      processingTime: null,
      error: null,
    }));
    setImages((prev) => [...prev, ...newImages]);
  }, []);

  // ── Enhance all pending images ──────────────────────────────────────────────
  const handleEnhanceAll = useCallback(async () => {
    const pending = images.filter((img) => img.status === 'pending');
    if (!pending.length) return;

    setIsProcessing(true);
    setImages((prev) =>
      prev.map((img) =>
        img.status === 'pending' ? { ...img, status: 'processing' } : img
      )
    );

    try {
      const files = pending.map((img) => img.file);
      const { results } = await enhanceBatch(files);

      setImages((prev) =>
        prev.map((img) => {
          const result = results.find((r) => r.filename === img.file.name);
          if (!result) return img;
          if (result.status === 'error') {
            return { ...img, status: 'error', error: result.error };
          }
          return {
            ...img,
            status: 'done',
            enhancedUrl: `data:image/png;base64,${result.enhanced_image}`,
            psnr: result.psnr,
            ssim: result.ssim,
            processingTime: result.processing_time,
          };
        })
      );

      const successCount = results.filter((r) => r.status === 'success').length;
      const errorCount = results.filter((r) => r.status === 'error').length;
      if (errorCount > 0) {
        showToast(`Enhanced ${successCount} image(s), ${errorCount} failed.`, 'error');
      } else {
        showToast(`Successfully enhanced ${successCount} image(s)! 🎉`, 'success');
      }
    } catch (err) {
      setImages((prev) =>
        prev.map((img) =>
          img.status === 'processing'
            ? { ...img, status: 'error', error: err.message }
            : img
        )
      );
      showToast(`Enhancement failed: ${err.message}`, 'error');
    } finally {
      setIsProcessing(false);
    }
  }, [images, showToast]);

  // ── UI handlers ─────────────────────────────────────────────────────────────
  const handleImageClick = useCallback((imageId) => {
    setSelectedImageId(imageId);
  }, []);

  const handleOpenLightbox = useCallback((url, type, imageId) => {
    setLightbox({ url, type, imageId });
  }, []);

  const handleCloseLightbox = useCallback(() => setLightbox(null), []);
  const handleCloseComparison = useCallback(() => setSelectedImageId(null), []);

  const handleDownloadAll = useCallback(() => {
    images
      .filter((img) => img.status === 'done' && img.enhancedUrl)
      .forEach((img) => {
        const a = document.createElement('a');
        a.href = img.enhancedUrl;
        a.download = `enhanced_${img.file.name}`;
        a.click();
      });
  }, [images]);

  const pendingCount = images.filter((img) => img.status === 'pending').length;
  const doneCount = images.filter((img) => img.status === 'done').length;

  return (
    <div className="enhancement-page">
      <UploadZone
        onFilesSelected={handleFilesSelected}
        onEnhanceAll={handleEnhanceAll}
        isProcessing={isProcessing}
        pendingCount={pendingCount}
      />

      {images.length > 0 && (
        <ImageGallery
          images={images}
          selectedImageId={selectedImageId}
          onImageClick={handleImageClick}
          onOpenLightbox={handleOpenLightbox}
          onCloseComparison={handleCloseComparison}
          onDownloadAll={handleDownloadAll}
          doneCount={doneCount}
        />
      )}

      {lightbox && (
        <Lightbox
          images={images}
          initialImageId={lightbox.imageId}
          initialType={lightbox.type}
          onClose={handleCloseLightbox}
        />
      )}

      {toast && (
        <div className={`enhancement-toast enhancement-toast--${toast.type}`}>
          {toast.message}
        </div>
      )}
    </div>
  );
}

export default EnhancementPage;

