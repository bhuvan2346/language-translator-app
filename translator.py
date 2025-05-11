# Import required libraries
from googletrans import Translator
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import pandas as pd

# Initialize session state for translation history
if "history" not in st.session_state:
    st.session_state.history = []

# Set page title and icon
st.set_page_config(page_title="🌍 Smart Translator", page_icon="🌍")

# App Title
st.title("🌍 Smart Language Translator")

# Language options
language_options = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te',
    'Tamil': 'ta',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Bengali': 'bn',
    'Marathi': 'mr',
    'Gujarati': 'gu',
    'Punjabi': 'pa',
    'Urdu': 'ur',
    'Odia': 'or',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko'
}

# Input text area
text = st.text_area("📝 Enter text to translate:")

# Dropdown for target language
target_language = st.selectbox("🎯 Choose target language", list(language_options.keys()))

# Translate Button
if st.button("🔄 Translate"):
    if text.strip() == "":
        st.warning("⚠️ Please enter some text!")
    else:
        # Create translator object
        translator = Translator()
        # Translate the text
        translated_text = translator.translate(text, dest=language_options[target_language])

        # Show result
        st.success(f"✅ Translation: {translated_text.text}")

        # Show detected source language
        st.info(f"🔤 Detected language: {translated_text.src} → Translated to: {translated_text.dest}")

        # Text-to-Speech
        st.info("🔊 Playing audio...")
        # Remove old audio file
        if os.path.exists("output.mp3"):
            os.remove("output.mp3")
        # Generate new audio
        tts = gTTS(translated_text.text, lang=language_options[target_language])
        tts.save("output.mp3")
        os.system("start output.mp3")  # Windows only

        # Save to history
        st.session_state.history.append({
            "input": text,
            "source": translated_text.src,
            "target": target_language,
            "translation": translated_text.text
        })

# Voice Input Button
if st.button("🎤 Speak"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙️ Listening...")
        audio = r.listen(source)
        try:
            spoken_text = r.recognize_google(audio)
            st.write("🗣️ You said:", spoken_text)

            # Translate after recognizing
            translator = Translator()
            translated_text = translator.translate(spoken_text, dest=language_options[target_language])

            st.success(f"✅ Translation: {translated_text.text}")
            st.info(f"🔤 Detected language: {translated_text.src} → Translated to: {translated_text.dest}")

            # Text-to-Speech
            if os.path.exists("output.mp3"):
                os.remove("output.mp3")
            tts = gTTS(translated_text.text, lang=language_options[target_language])
            tts.save("output.mp3")
            os.system("start output.mp3")

            # Save to history
            st.session_state.history.append({
                "input": spoken_text,
                "source": translated_text.src,
                "target": target_language,
                "translation": translated_text.text
            })

        except:
            st.error("❌ Could not understand audio.")

# Show Translation History
if st.session_state.history:
    st.markdown("📜 **Translation History**")
    st.table(pd.DataFrame(st.session_state.history))
else:
    st.markdown("📂 *No translations yet.*")