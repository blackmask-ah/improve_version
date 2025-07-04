import streamlit as st
from TTS.api import TTS
import tempfile
import os
import random

# Sample phrases to make a positive impact
sample_phrases = [
    "Welcome to BlackMask – where innovation meets voice.",
    "Experience the future of AI voice synthesis, right here.",
    "This is a demo of our cutting-edge neural text-to-speech engine.",
    "Empowering your app with realistic, human-like speech.",
    "Your content deserves a voice – let's bring it to life!"
]

st.set_page_config(page_title="🗣 Realistic Neural TTS", page_icon="🔊")
st.title("🗣 High-Quality Neural TTS (Coqui TTS)")

# Choose a random phrase for initial text
default_text = random.choice(sample_phrases)

text = st.text_area("Enter text to synthesize", default_text)

# Initialize TTS model once
@st.cache_resource
def load_model():
    return TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

tts = load_model()

# Select speaker
speaker = st.selectbox("Select a speaker voice", tts.speakers)

if st.button("🎙 Generate Realistic Voice"):
    with st.spinner("🛠 Generating speech... Please wait."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            temp_file = fp.name
            tts.tts_to_file(text=text, speaker=speaker, file_path=temp_file)

        st.success("✅ Voice generated successfully!")
        st.audio(temp_file, format="audio/wav")
        with open(temp_file, "rb") as f:
            st.download_button("⬇️ Download Audio", f, file_name="output.wav", mime="audio/wav")
        os.remove(temp_file)
