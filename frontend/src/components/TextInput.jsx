import React from "react";

function TextInput({ text, setText }) {

  return (
    <div className="text-input-container">

      <label className="input-label">
      </label>

      <textarea
        className="text-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={12}
      />

    </div>
  );

}

export default TextInput;