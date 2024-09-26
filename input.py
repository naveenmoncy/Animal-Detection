# from animals import callback
# import streamlit as st
# import time
# import cv2
# import numpy as np
# from streamlit_webrtc import webrtc_streamer
# import av
# import supervision as sv
# from inference.models.utils import get_roboflow_model
# import pygame
# from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase


# def webcam_input(sound_files, model, tracker, box_annotator, label_annotator, trace_annotator, names, animal_log):
#     flip = st.checkbox("Flip Camera")
#     def video_frame_callback(frame):
#             img = frame.to_ndarray(format="bgr24")

#             img, detected_class_id = callback(img, 0, model, tracker, box_annotator, label_annotator, trace_annotator, names, sound_files, animal_log)

#             if detected_class_id is not None:
#                 sound_file = sound_files.get(detected_class_id)
#                 if sound_file is not None:
#                     pygame.mixer.init()
#                     pygame.mixer.music.load(sound_file)
#                     pygame.mixer.music.play()
#                     pygame.time.wait(300)
#                     pygame.mixer.music.stop()

#             flipped = img[::-1,:,:] if flip else img

#             return av.VideoFrame.from_ndarray(flipped, format="bgr24")
    

#     webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

# def start_streaming(sound_files, model, tracker, box_annotator, label_annotator, trace_annotator, names, animal_log):
#     class VideoProcessor(VideoProcessorBase):
#         def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
#             img = frame.to_ndarray(format="bgr24")
#             annotated_frame = callback(img, 0, model, tracker, box_annotator, label_annotator, trace_annotator, names, sound_files, animal_log)
#             return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")

#     webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor, rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}) )

#     if webrtc_ctx.video_processor:
#         if st.button('Stop'):
#             webrtc_ctx.video_processor.stop()