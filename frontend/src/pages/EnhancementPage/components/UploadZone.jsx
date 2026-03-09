import { useState, useRef, useCallback } from "react";
import "./UploadZone.css";

const ACCEPTED_TYPES = [
  "image/jpeg",
  "image/png",
  "image/tiff",
  "image/bmp",
  "image/webp",
];

function UploadZone({
  onFilesSelected,
  onEnhanceAll,
  isProcessing,
  pendingCount,
}) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const filterFiles = (fileList) =>
    Array.from(fileList).filter((f) => ACCEPTED_TYPES.includes(f.type));

  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!e.currentTarget.contains(e.relatedTarget)) {
      setIsDragging(false);
    }
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      const files = filterFiles(e.dataTransfer.files);
      if (files.length) onFilesSelected(files);
    },
    [onFilesSelected],
  );

  const handleFileChange = useCallback(
    (e) => {
      const files = filterFiles(e.target.files);
      if (files.length) onFilesSelected(files);
      e.target.value = "";
    },
    [onFilesSelected],
  );

  const handleZoneClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  return (
    <section className="upload-section">
      <div
        className={`upload-zone${isDragging ? " upload-zone--dragging" : ""}`}
        onClick={handleZoneClick}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && handleZoneClick()}
        aria-label="Upload images by clicking or dragging files here"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".jpg,.jpeg,.png,.tiff,.tif,.bmp,.webp"
          multiple
          className="upload-input"
          onChange={handleFileChange}
        />

        <div className="upload-icon">{isDragging ? "📂" : "📤"}</div>
        <h2 className="upload-title">
          {isDragging
            ? "Release to upload"
            : "Drop images here or click to browse"}
        </h2>
        <p className="upload-hint">
          Supports JPG, PNG, TIFF, BMP — multiple files allowed
        </p>
      </div>

      {pendingCount > 0 && (
        <div className="upload-actions">
          <span className="upload-count">
            {pendingCount} image{pendingCount !== 1 ? "s" : ""} ready to enhance
          </span>
          <button
            className={`btn-enhance${isProcessing ? " btn-enhance--loading" : ""}`}
            onClick={onEnhanceAll}
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <span className="spinner" />
                Enhancing…
              </>
            ) : (
              <>✨ Enhance All</>
            )}
          </button>
        </div>
      )}
    </section>
  );
}

export default UploadZone;
