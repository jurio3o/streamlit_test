import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder()

if audio_bytes: # audio_bytes에 음성이 녹음됨! => 지금은 자동으로 녹음,, 소리가 끊어지면 바로 녹음 중단.
    st.audio(audio_bytes, format="audio/wav")

    if st.download_button('Download file', audio_bytes):
        st.write('thank you')