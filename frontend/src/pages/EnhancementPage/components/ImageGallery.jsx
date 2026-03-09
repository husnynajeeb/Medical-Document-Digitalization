import { useCallback } from 'react';
import ComparisonSlider from './ComparisonSlider.jsx';
import MetricsCard from './MetricsCard.jsx';
import './ImageGallery.css';

const STATUS_LABELS = {
  pending: 'Pending',
  processing: 'Processing…',
  done: 'Enhanced ✅',
  error: 'Failed ❌',
};

function ImageCard({ image, isSelected, onCardClick, onOpenLightbox, onCloseComparison }) {
  const handleDownload = useCallback(
    (e) => {
      e.stopPropagation();
      const a = document.createElement('a');
      a.href = image.enhancedUrl;
      a.download = `enhanced_${image.file.name}`;
      a.click();
    },
    [image]
  );

  return (
    <div className={`image-card glass${isSelected ? ' image-card--selected' : ''}`}>
      <div className="image-card-thumb" onClick={() => onCardClick(image.id)}>
        <img
          src={image.originalUrl}
          alt={image.file.name}
          className="image-card-img"
          loading="lazy"
        />
        <span className={`status-badge status-badge--${image.status}`}>
          {STATUS_LABELS[image.status] || image.status}
        </span>
      </div>

      <div className="image-card-body">
        <p className="image-card-name" title={image.file.name}>
          {image.file.name}
        </p>

        {image.status === 'done' && (
          <MetricsCard
            psnr={image.psnr}
            ssim={image.ssim}
            processingTime={image.processingTime}
          />
        )}

        {image.status === 'error' && (
          <p className="image-card-error">{image.error || 'Unknown error'}</p>
        )}

        {image.status === 'done' && image.enhancedUrl && (
          <button className="btn-download" onClick={handleDownload}>
            ⬇ Download Enhanced
          </button>
        )}
      </div>

      {/* Inline comparison slider modal */}
      {isSelected && image.status === 'done' && (
        <div className="comparison-overlay" onClick={(e) => e.stopPropagation()}>
          <button
            className="comparison-close"
            onClick={onCloseComparison}
            aria-label="Close comparison"
          >
            ✕
          </button>
          <ComparisonSlider
            originalUrl={image.originalUrl}
            enhancedUrl={image.enhancedUrl}
            onOpenLightbox={(url, type) => onOpenLightbox(url, type, image.id)}
          />
        </div>
      )}
    </div>
  );
}

function ImageGallery({
  images,
  selectedImageId,
  onImageClick,
  onOpenLightbox,
  onCloseComparison,
  onDownloadAll,
  doneCount,
}) {
  return (
    <section className="gallery-section">
      <div className="gallery-header">
        <h2 className="gallery-title">
          Images
          <span className="gallery-count">{images.length}</span>
        </h2>
        {doneCount > 0 && (
          <button className="btn-download-all" onClick={onDownloadAll}>
            ⬇ Download All Enhanced ({doneCount})
          </button>
        )}
      </div>

      <div className="gallery-grid">
        {images.map((image) => (
          <ImageCard
            key={image.id}
            image={image}
            isSelected={selectedImageId === image.id}
            onCardClick={onImageClick}
            onOpenLightbox={onOpenLightbox}
            onCloseComparison={onCloseComparison}
          />
        ))}
      </div>
    </section>
  );
}

export default ImageGallery;
