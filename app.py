import logging
import os.path
from dataclasses import dataclass

import streamlit as st
import numpy as np
import pandas as pd
import io
from PIL import Image


@dataclass
class App:
    start_time: int = 0


app: App = st.session_state.get("app")

if not app:
    app = App()
    logging.info("creating new app instance")
    st.session_state.app = app

qa_model = None


video = os.path.join("data", "Neurons and the brain.mp4")

st.video(video, start_time=app.start_time)

# Define a function to answer a question about a video
def answer_question(question, video_url):
    # Get the video snip of the explanation
    video_snip =

    # Answer the question using the QA model
    answer = qa_model.answer(question, video_snip)

    # Return the answer and the video snip
    return answer, video_snip


# Set the title of the app
st.title("Learning Video with Question Answering")

# Display the video
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Ask the user a question about the video
question = st.text_input("Ask a question about the video:")

# Answer the question and display the video snip
if question:
    answer, video_snip = answer_question(question, video_url)

    st.write(answer)
    st.image(video_snip)
