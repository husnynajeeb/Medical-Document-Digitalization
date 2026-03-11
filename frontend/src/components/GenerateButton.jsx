import React from "react";

function GenerateButton({ onClick }) {
  return (
    <button onClick={onClick} className="generate-btn">
      Generate Translation
    </button>
  );
}

export default GenerateButton;