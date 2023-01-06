import logging
import logging.handlers
import queue
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List

import av
import numpy as np
import pydub
import streamlit as st

import requests
import json
import STT

from streamlit_webrtc import WebRtcMode, webrtc_streamer

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)

 
# This code is based on https://github.com/streamlit/demo-self-driving/blob/230245391f2dda0cb464008195a470751c01770b/streamlit_app.py#L48  # noqa: E501
# def download_file(url, download_to: Path, expected_size=None):
#     # Don't download the file twice.
#     # (If possible, verify the download using the file length.)
#     if download_to.exists():
#         if expected_size:
#             if download_to.stat().st_size == expected_size:
#                 return
#         else:
#             st.info(f"{url} is already downloaded.")
#             if not st.button("Download again?"):
#                 return

#     download_to.parent.mkdir(parents=True, exist_ok=True)

#     # These are handles to two visual elements to animate.
#     weights_warning, progress_bar = None, None
#     try:
#         weights_warning = st.warning("Downloading %s..." % url)
#         progress_bar = st.progress(0)
#         with open(download_to, "wb") as output_file:
#             with urllib.request.urlopen(url) as response:
#                 length = int(response.info()["Content-Length"])
#                 counter = 0.0
#                 MEGABYTES = 2.0 ** 20.0
#                 while True:
#                     data = response.read(8192)
#                     if not data:
#                         break
#                     counter += len(data)
#                     output_file.write(data)

#                     # We perform animation by overwriting the elements.
#                     weights_warning.warning(
#                         "Downloading %s... (%6.2f/%6.2f MB)"
#                         % (url, counter / MEGABYTES, length / MEGABYTES)
#                     )
#                     progress_bar.progress(min(counter / length, 1.0))
#     # Finally, we remove these visual elements by calling .empty().
#     finally:
#         if weights_warning is not None:
#             weights_warning.empty()
#         if progress_bar is not None:
#             progress_bar.empty()


def main():
    st.header("시켜줘 보아즈 명예 경찰관")
    st.markdown(
        """
ViTo STT 적용을 위한 실험 페이지
"""
    )

    # https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3
    # MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"  # noqa
    # LANG_MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"  # noqa
    # MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.pbmm"
    # LANG_MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.scorer"

    # download_file(MODEL_URL, MODEL_LOCAL_PATH, expected_size=188915987)
    # download_file(LANG_MODEL_URL, LANG_MODEL_LOCAL_PATH, expected_size=953363776)

    # lm_alpha = 0.931289039105002
    # lm_beta = 1.1834137581510284
    # beam = 100

    app_sst()



def app_sst():
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": False, "audio": True},
    )

    status_indicator = st.empty()

    if not webrtc_ctx.state.playing:
        return

    status_indicator.write("Loading...")
    text_output = st.empty()
    stream = None

    while True:
        if webrtc_ctx.audio_receiver:
            if stream is None:
                # from deepspeech import Model

                # model = Model(model_path)
                # model.enableExternalScorer(lm_path)
                # model.setScorerAlphaBeta(lm_alpha, lm_beta)
                # model.setBeamWidth(beam)

                # stream = model.createStream()

                status_indicator.write("Model loaded.")

            sound_chunk = pydub.AudioSegment.empty()
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                status_indicator.write("No frame arrived.")
                continue

            status_indicator.write("Running. Say something!")

            for audio_frame in audio_frames:
                # sound에 브라우저를 통해 녹음하는 소리가 저장됨
                # text_output.markdown(f"========================")
                # text_output.markdown(f"audio_frame {type(audio_frame)}")
                sound = pydub.AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                # 실시간으로 녹음되는 것들을 합치는 과정인듯
                # text_output.markdown(f"sound {type(sound)}")
                sound_chunk += sound
            
            if len(sound_chunk) > 0:
                # set_channels(1): 인자값이 1이면 모노, 2면 스테레오라는데,,, 잘 모르겠음 쨌든 기본 값은 1이라 그대로 유지
                # set_frame_rate(): 음질의 품질을 이야기 하는 것 같은데,, 잘 모르겠네
                # text_output.markdown(f"sound_chunk: {type(sound_chunk)}")
                sound_chunk = sound_chunk.set_channels(1)
                # text_output.markdown(f"sound_chunk: {type(sound_chunk)}")
                sound_chunk.export("./test.mp3", format="mp3")

                # buffer = np.array(sound_chunk.get_array_of_samples())
                # buffer 상태 확인
                # text_output.markdown(f"buffer: {type(buffer)}")
                # stream: 모델에 
                # stream.feedAudioContent(buffer)
                # text = stream.intermediateDecode()
                text_output.markdown(f"**Text:** {text}")
        else:
            status_indicator.write("AudioReciver is not set. Abort.")
            break




if __name__ == "__main__":
    import os

    DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
        "%(message)s",
        force=True,
    )

    logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

    st_webrtc_logger = logging.getLogger("streamlit_webrtc")
    st_webrtc_logger.setLevel(logging.DEBUG)

    fsevents_logger = logging.getLogger("fsevents")
    fsevents_logger.setLevel(logging.WARNING)

    main()