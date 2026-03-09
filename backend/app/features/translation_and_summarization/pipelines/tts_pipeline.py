from gtts import gTTS
import io

def generate_tts(text, lang):

    mp3_buffer = io.BytesIO()

    tts = gTTS(
        text=text,
        lang=lang
    )

    tts.write_to_fp(mp3_buffer)

    mp3_buffer.seek(0)

    return mp3_buffer