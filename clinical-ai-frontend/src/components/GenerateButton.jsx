import React from "react";

function GenerateButton({ onClick }) {
  return (
    <button onClick={onClick}>
      Generate Translation
    </button>
  );
}

export default GenerateButton;