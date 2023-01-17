import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr
import STT

# import numpy as np
# from scipy.io.wavfile import write
# import soundfile as sf
# import wave
# import streamlit.components.v1 as components
# import os

# sound_chunk = pydub.AudioSegment.empty()

# for audio_frame in audio_bytes:
#     sound = pydub.AudioSegment(
#                         data=audio_frame.to_ndarray().tobytes(),
#                         sample_width=audio_frame.format.bytes,
#                         frame_rate=audio_frame.sample_rate,
#                         channels=len(audio_frame.layout.channels),
#                     )
#     sound_chunk += sound

# sound.export('./testttt.wav', format='wav')
st.title("Audio Recorder")


audio_bytes = audio_recorder("Click to record", pause_threshold=10.0)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

AudioSegment.from_raw(BytesIO(audio_bytes), sample_width=2, frame_rate=32000, channels=2).export('./testttt.wav', format='wav')
# wav_file = open("audio.wav", "wb")
# wav_file.write(audio_bytes.tobytes()).export('./asdf.wav', format = 'wav')

r = sr.Recognizer()

test = sr.AudioFile('./testttt.wav')
with test as source:
    audio = r.record(source)


# result = r.recognize_google(audio, language = 'ko-KR', show_all=True)['alternative']
# rr = []
# for i in result:
#     rr.append(i['transcript'])
# rr = '.'.join(rr)
# st.markdown(f'{rr}')
text = STT.BitoGet(STT.BitoPost(audio))
st.markdown(text)