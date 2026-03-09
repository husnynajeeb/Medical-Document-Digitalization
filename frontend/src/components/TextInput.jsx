import React from "react";

function TextInput({ text, setText }) {

  return (
    <div className="text-input-container">

      <label className="input-label">
        Clinical Note
      </label>

      <textarea
        className="text-input"
        placeholder={`Example:
Patient presents with uncontrolled diabetes.
Recent Labs:
HbA1c 9.2%
Current Medications:
Metformin 500mg
Assessment:
Poor glycemic control
Plan:
Start insulin therapy`}
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={12}
      />

    </div>
  );

}

export default TextInput;