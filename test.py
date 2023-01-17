import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr
import STT

# # import numpy as np
# # from scipy.io.wavfile import write
# # import soundfile as sf
# # import wave
# # import streamlit.components.v1 as components
# # import os

# # sound_chunk = pydub.AudioSegment.empty()

# # for audio_frame in audio_bytes:
# #     sound = pydub.AudioSegment(
# #                         data=audio_frame.to_ndarray().tobytes(),
# #                         sample_width=audio_frame.format.bytes,
# #                         frame_rate=audio_frame.sample_rate,
# #                         channels=len(audio_frame.layout.channels),
# #                     )
# #     sound_chunk += sound

# # sound.export('./testttt.wav', format='wav')
# st.title("Audio Recorder")


# audio_bytes = audio_recorder("Click to record", pause_threshold=10.0)
# if audio_bytes:
#     st.audio(audio_bytes, format="audio/wav")

# AudioSegment.from_raw(BytesIO(audio_bytes), sample_width=2, frame_rate=32000, channels=2).export('./testttt.wav', format='wav')
# # wav_file = open("audio.wav", "wb")
# # wav_file.write(audio_bytes.tobytes()).export('./asdf.wav', format = 'wav')

# r = sr.Recognizer()

# test = sr.AudioFile('./testttt.wav')
# with test as source:
#     audio = r.record(source)




# # result = r.recognize_google(audio, language = 'ko-KR', show_all=True)['alternative']
# # rr = []
# # for i in result:
# #     rr.append(i['transcript'])
# # rr = '.'.join(rr)
# # st.markdown(f'{rr}')
# # text = STT.BitoGet(STT.BitoPost(audio))
# # st.markdown(text)

import wave
from dataclasses import dataclass, asdict
import STT

import pyaudio


@dataclass
class StreamParams:
    format: int = pyaudio.paInt16
    channels: int = 2
    rate: int = 44100
    frames_per_buffer: int = 1024
    input: bool = True
    output: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class Recorder:
    """Recorder uses the blocking I/O facility from pyaudio to record sound
    from mic.
    Attributes:
        - stream_params: StreamParams object with values for pyaudio Stream
            object
    """
    def __init__(self, stream_params: StreamParams) -> None:
        self.stream_params = stream_params
        self._pyaudio = None
        self._stream = None
        self._wav_file = None

    def record(self, duration: int, save_path: str) -> None:
        """Record sound from mic for a given amount of seconds.
        :param duration: Number of seconds we want to record for
        :param save_path: Where to store recording
        """
        print("Start recording...")
        self._create_recording_resources(save_path) 
        self._write_wav_file_reading_from_stream(duration) # 이걸 반복해야 함
        self._close_recording_resources() 
        print("Stop recording")

    def _create_recording_resources(self, save_path: str) -> None: # 빈 오디오 생성 
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(**self.stream_params.to_dict())
        self._create_wav_file(save_path)

    def _create_wav_file(self, save_path: str): # 오디오 저장할 빈 wav파일 열기 
        self._wav_file = wave.open(save_path, "wb")
        self._wav_file.setnchannels(self.stream_params.channels)
        self._wav_file.setsampwidth(self._pyaudio.get_sample_size(self.stream_params.format))
        self._wav_file.setframerate(self.stream_params.rate)

    def _write_wav_file_reading_from_stream(self, duration: int) -> None: # n초동안 녹음 => end button 을 누를 때까지 반복 시킬 것
        for _ in range(int(self.stream_params.rate * duration / self.stream_params.frames_per_buffer)):
            audio_data = self._stream.read(self.stream_params.frames_per_buffer)
            self._wav_file.writeframes(audio_data)
        text = STT.BitoGet(STT.BitoPost('C://Users/Administrator/Dropbox/adv/test/audio.wav')) # audio.wav를 close 하지 않아도 불러오면 음성이 누적되어있는 파일을 stt 할 수 있음 => 로컬에서,,
        st.markdown(text)

        # ★★★★★ py audio를 streamlit에 올렸을 때 어떻게 돌아가는지 알아야함 or streamlit audio recorder 로 바꿀 수 있는지 .. => 로컬에서 실행가능한지도  ★★★★★
        # stt api가 무조건 저장되어있는 파일을 불러와서 stt 해야하는지 파악해야함
        # 현재 vito api가 바로 변환을 안해줘서 너무 느림 
        # text를 model 함수 불러와서 바로 넣을 수 있도록 해야 함

    def _close_recording_resources(self) -> None: # (st.button end  버튼 누르면 끝낼 수 있게 )pyaudio 끝내기
        self._wav_file.close()
        self._stream.close()
        self._pyaudio.terminate()


Recorder()

# if __name__ == "__main__":
#     stream_params = StreamParams()
#     recorder = Recorder(stream_params)
#     recorder.record(5, "audio.wav")

