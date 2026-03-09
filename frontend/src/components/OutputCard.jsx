import React from "react";
import { generateSpeech } from "../services/api";

function OutputCard({ output, lang }) {

  if (!output) return null;

  const handlePlayVoice = async (text) => {

    try {

      const audio = await generateSpeech({
        text: text,
        target_lang: lang
      });

      const audioPlayer = new Audio(audio);
      audioPlayer.play();

    } catch (error) {
      console.error("TTS Error:", error);
    }

  };

  /* ===============================
     SIMPLE OUTPUT
  =============================== */

  if (typeof output === "string") {

    return (
      <div className="output-card">

        <div className="output-header">
          <h3>Result</h3>

          <button
            className="voice-btn"
            onClick={() => handlePlayVoice(output)}
          >
            🔊 Play Voice
          </button>
        </div>

        <p className="section-text">{output}</p>

      </div>
    );

  }

  /* ===============================
     SECTION OUTPUT
  =============================== */

  return (

    <div className="output-card">

      {Object.keys(output).map((section) => {

        const text = output[section];

        if (!text) return null;

        return (

          <div key={section} className="section-block">

            <div className="output-header">

              <h3>{section}</h3>

              <button
                className="voice-btn"
                onClick={() => handlePlayVoice(text)}
              >
                🔊 Play Voice
              </button>

            </div>

            <p className="section-text">
              {text}
            </p>

          </div>

        );

      })}

    </div>

  );

}

export default OutputCard;