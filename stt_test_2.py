import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder()
if audio_bytes:
    audio = st.audio(audio_bytes, format="audio/wav")

    
    if st.download_button('Download file', audio):
        st.write('thank you')