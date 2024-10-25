import google.generativeai as genai
import os
import fitz
import streamlit as sm
from gtts import gTTS
import tempfile

sample=sm.file_uploader("Upload pdf", type=["pdf"])

def text_to_speech(text):
    tts=gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix="mp3") as tmpfile:
        tts.save(tmpfile.name)
        return tmpfile.name

if sample is not None:
    doc=fitz.open(stream=sample.read(), filetype="pdf")
    text=""
    for page in doc:
        text+=page.get_text()
    genai.configure(api_key=os.getenv(""))
    model = genai.GenerativeModel("gemini-pro")
    response=model.generate_content("Give me 10 interview questions from the following texts extracted from the resume, use a terminating symbol '&' after every question: \n"+text)
    resultfromprompt=response.text
    questions=resultfromprompt.split('&')
    if sm.button(label="Generate questions", type="primary"):
        for a in questions:
            if a:
            	a.strip()
            	sm.write(a)
            	audio_file=text_to_speech(a)
            	audio_bytes=open(audio_file, 'rb').read()
            	sm.audio(audio_bytes, format="audio/mp3")
