import { useState, useEffect, useCallback } from 'react';
import './Lightbox.css';

function Lightbox({ images, initialImageId, initialType, onClose }) {
  const { t } = useLanguage();

  const viewableImages = images.filter(
    (img) => img.status === 'done' && img.enhancedUrl
  );

  const [currentIndex, setCurrentIndex] = useState(() => {
    const idx = viewableImages.findIndex((img) => img.id === initialImageId);
    return idx >= 0 ? idx : 0;
  });

  const [viewType, setViewType] = useState(initialType || 'enhanced');

  const currentImage = viewableImages[currentIndex];

  const imageUrl =
    viewType === 'enhanced' && currentImage?.enhancedUrl
      ? currentImage.enhancedUrl
      : currentImage?.originalUrl;

  const handlePrev = useCallback(() => {
    setCurrentIndex(
      (i) => (i - 1 + viewableImages.length) % viewableImages.length
    );
  }, [viewableImages.length]);

  const handleNext = useCallback(() => {
    setCurrentIndex((i) => (i + 1) % viewableImages.length);
  }, [viewableImages.length]);

  const toggleType = useCallback(() => {
    setViewType((t) => (t === 'enhanced' ? 'original' : 'enhanced'));
  }, []);

  // Keyboard support
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'ArrowLeft') handlePrev();
      if (e.key === 'ArrowRight') handleNext();
    };

    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose, handlePrev, handleNext]);

  // Prevent scroll
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = '';
    };
  }, []);

  if (!currentImage) return null;

  return (
    <div className="lightbox-backdrop" onClick={onClose}>
      <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>

        {/* CLOSE */}
        <button
          className="lightbox-close"
          onClick={onClose}
          aria-label={t('close')}
        >
          ✕
        </button>

        {/* TOOLBAR */}
        <div className="lightbox-toolbar">
          
          <button
            className={`lightbox-toggle${viewType === 'original' ? ' active' : ''}`}
            onClick={toggleType}
          >
            {viewType === 'enhanced'
              ? `👁 ${t('view_original') || 'View Original'}`
              : `✨ ${t('view_enhanced') || 'View Enhanced'}`}
          </button>

          <span className="lightbox-filename">
            {currentImage.file.name}
          </span>
        </div>

        {/* IMAGE */}
        <div className="lightbox-img-wrapper">
          <img
            src={imageUrl}
            alt={viewType}
            className="lightbox-img"
            draggable={false}
          />
        </div>

        {/* NAVIGATION */}
        {viewableImages.length > 1 && (
          <>
            <button
              className="lightbox-nav lightbox-nav--prev"
              onClick={handlePrev}
              aria-label={t('previous')}
            >
              ‹
            </button>

            <button
              className="lightbox-nav lightbox-nav--next"
              onClick={handleNext}
              aria-label={t('next')}
            >
              ›
            </button>

            <div className="lightbox-counter">
              {currentIndex + 1} / {viewableImages.length}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Lightbox;