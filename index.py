from animals import callback
import streamlit as st
import time
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av
import supervision as sv
from inference.models.utils import get_roboflow_model
import pygame
from streamlit.runtime.scriptrunner import get_script_run_ctx, add_script_run_ctx
from threading import Thread
from mail import send_email



check_data=[]





def play_sound(sound_file, class_name,frame):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    check_data.append({
        "time": time.time(),
        "class_name": class_name
    })
    
    if(check_data[-1]["time"] - check_data[0]["time"] >= 10):
        send_email(frame, "Wildlife Detected", f"A {check_data[0]['class_name']} has been detected in the area")
        check_data.clear()
    pygame.time.wait(1000)
    pygame.mixer.music.stop()

def play_sound_thread(sound_file,class_name,frame):
    thread_one = Thread(target=play_sound, args=(sound_file,class_name,frame))
    add_script_run_ctx(thread_one,class_name)
    thread_one.start()

sound_files = {
    1: 'Gunshot.mp3',
    0: 'Bees.mp3',
 
}

model = get_roboflow_model(model_id="animal-classification-tima/5", api_key="69m1zkCJhpHpTvN4WOIV")
tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()
names=["Boar", "Elephant", "Giraffe", "Horse", "Lion", "Polar Bear", "Tiger", "Zebra"]

animal_log={}

detected_animal_placeholder = st.empty()

st.title('Welcome to Wildlife Detection App')

st.subheader('Video Upload and Display')

start_button = st.button("Start Video")

animal_detected = False

st.toast("Welcome to Wildlife Detection App")

flip = st.checkbox("Flip Camera")
def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")

        img, detected_class_id = callback(img, 0, model, tracker, box_annotator, label_annotator, trace_annotator, names, sound_files, animal_log)

        if detected_class_id is not None:
            animal_detected = False
            sound_file = sound_files.get(detected_class_id)
            if sound_file is not None:
                play_sound_thread(sound_file,names[detected_class_id],frame=img)


        flipped = img[::-1,:,:] if flip else img

        return av.VideoFrame.from_ndarray(flipped, format="bgr24")

if animal_detected:
    st.toast("Animal Detected")
    # Reset the global variable
    animal_detected = False

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)



