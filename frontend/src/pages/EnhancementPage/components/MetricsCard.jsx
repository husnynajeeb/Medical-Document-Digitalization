import './MetricsCard.css';

function grade(psnr, ssim) {
  if (psnr === null && ssim === null) return 'neutral';
  const psnrOk = psnr === null || psnr > 25;
  const ssimOk = ssim === null || ssim > 0.85;
  const psnrMid = psnr === null || psnr > 20;
  const ssimMid = ssim === null || ssim > 0.7;

  if (psnrOk && ssimOk) return 'good';
  if (psnrMid && ssimMid) return 'moderate';
  return 'low';
}

function MetricsCard({ psnr, ssim, processingTime }) {
  const quality = grade(psnr, ssim);

  return (
    <div className={`metrics-card metrics-card--${quality}`}>
      <div className="metrics-row">
        {psnr !== null && psnr !== undefined ? (
          <div className="metric">
            <span className="metric-label">PSNR</span>
            <span className="metric-value">{psnr.toFixed(1)} dB</span>
          </div>
        ) : null}

        {ssim !== null && ssim !== undefined ? (
          <div className="metric">
            <span className="metric-label">SSIM</span>
            <span className="metric-value">{ssim.toFixed(4)}</span>
          </div>
        ) : null}

        {processingTime !== null && processingTime !== undefined ? (
          <div className="metric">
            <span className="metric-label">Time</span>
            <span className="metric-value">{processingTime.toFixed(2)}s</span>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default MetricsCard;
