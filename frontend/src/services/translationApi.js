export const processMedicalImage = async (base64Image, lang = "en") => {
  const response = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input_type: "image",
      image: base64Image,
      target_lang: lang,
      summarize: true,
    }),
  });

  if (!response.ok) {
    throw new Error("Processing failed");
  }

  return await response.json();
};