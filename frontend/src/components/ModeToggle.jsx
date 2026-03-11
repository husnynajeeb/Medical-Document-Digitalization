import React from "react";

function ModeToggle({ summarize, setSummarize }) {

  return (
    <div className="mode-toggle">

      <label className="toggle-label">

        <input
          type="checkbox"
          checked={summarize}
          onChange={() => setSummarize(!summarize)}
        />

        <span className="toggle-text">
          Enable Clinical Summarization
        </span>

      </label>

    </div>
  );

}

export default ModeToggle;