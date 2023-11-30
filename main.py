import logging

import streamlit as st

from config.constants import DEVELOPMENT, MODE
from enums.app import App
from utils.helpers_youtube import is_valid_youtube_url
from views.sidebar import sidebar

st.set_page_config(
    page_title="Boteach",
    page_icon=":books:",
)

st.title("Boteach")

sidebar()


app: App = st.session_state.get("app")

if not app or MODE == DEVELOPMENT:
    app = App()
    logging.info("creating new app instance")
    st.session_state.app = app

video_url = st.text_input("Paste the youtube url of your lesson", value=app.video)

if video_url and is_valid_youtube_url(video_url):
    logging.info(f"valid youtube url: {video_url}")
else:
    st.error("invalid youtube url")
    st.stop()

app.video = video_url

st.video(app.video, start_time=0)


st.header("Q/A Genie")
user_question = st.text_input("Ask a question about the video:")


if user_question and st.button("Submit", type="secondary"):
    with st.spinner("LLM Processing"):
        response = app.process_question(user_question)

        with st.chat_message("ai", avatar="assistant"):
            # response.answer = response.answer.replace("[7†source]", "") FIXME: not working
            st.markdown(response.answer)

        st.video(app.video, start_time=response.start_time)
