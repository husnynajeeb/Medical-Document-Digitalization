import { useState, useRef, useCallback, useEffect } from 'react';
import './ComparisonSlider.css';

function ComparisonSlider({ originalUrl, enhancedUrl, onOpenLightbox }) {
  const [sliderPos, setSliderPos] = useState(50); // percentage 0-100
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef(null);

  const getPositionFromEvent = useCallback((clientX) => {
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    return Math.min(100, Math.max(0, (x / rect.width) * 100));
  }, []);

  const startDrag = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onMove = useCallback(
    (clientX) => {
      if (!isDragging) return;
      setSliderPos(getPositionFromEvent(clientX));
    },
    [isDragging, getPositionFromEvent]
  );

  const stopDrag = useCallback(() => setIsDragging(false), []);

  // Mouse events
  useEffect(() => {
    const handleMouseMove = (e) => onMove(e.clientX);
    const handleMouseUp = () => stopDrag();

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, onMove, stopDrag]);

  // Touch events
  const handleTouchMove = useCallback(
    (e) => {
      if (!isDragging) return;
      e.preventDefault();
      onMove(e.touches[0].clientX);
    },
    [isDragging, onMove]
  );

  const handleTouchEnd = useCallback(() => stopDrag(), [stopDrag]);

  return (
    <div
      ref={containerRef}
      className="slider-container"
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {/* Original (bottom layer) */}
      <img
        src={originalUrl}
        alt="Original"
        className="slider-img slider-img--original"
        draggable={false}
        onClick={() => onOpenLightbox?.(originalUrl, 'original')}
      />

      {/* Enhanced (clipped on top) */}
      <img
        src={enhancedUrl}
        alt="Enhanced"
        className="slider-img slider-img--enhanced"
        style={{ clipPath: `inset(0 0 0 ${sliderPos}%)` }}
        draggable={false}
        onClick={() => onOpenLightbox?.(enhancedUrl, 'enhanced')}
      />

      {/* Labels */}
      <span className="slider-label slider-label--left">Original</span>
      <span className="slider-label slider-label--right">Enhanced</span>

      {/* Divider */}
      <div
        className={`slider-divider${isDragging ? ' slider-divider--dragging' : ''}`}
        style={{ left: `${sliderPos}%` }}
        onMouseDown={startDrag}
        onTouchStart={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        role="slider"
        aria-valuenow={Math.round(sliderPos)}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Comparison divider"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'ArrowLeft') setSliderPos((p) => Math.max(0, p - 2));
          if (e.key === 'ArrowRight') setSliderPos((p) => Math.min(100, p + 2));
        }}
      >
        <div className="slider-handle">
          <span className="slider-arrow">‹</span>
          <span className="slider-arrow">›</span>
        </div>
      </div>
    </div>
  );
}

export default ComparisonSlider;
