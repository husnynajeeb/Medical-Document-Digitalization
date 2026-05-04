import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: `${API_BASE_URL}/translation`,
  // timeout: 60000
});

/* ================================
   TRANSLATION API
================================ */

export const translateText = async (data) => {
  try {
    const response = await API.post("/translate", data);

    return response.data;
  } catch (error) {
    console.error("Translation API Error:", error);

    throw new Error("Translation failed. Please try again.");
  }
};

/* ================================
   TEXT TO SPEECH API
================================ */

export const generateSpeech = async (data) => {
  try {
    const response = await API.post("/tts", data, {
      responseType: "blob",
    });

    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error("TTS API Error:", error);

    throw new Error("Voice generation failed.");
  }
};
