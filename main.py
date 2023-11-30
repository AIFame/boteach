import logging

import streamlit as st
from pytube import YouTube

from config.constants import DEVELOPMENT, MODE
from enums.app import App
from views.sidebar import sidebar


def is_valid_youtube_url(url):
    try:
        YouTube(url)
        return True
    except Exception as e:
        logging.exception(f"youtube url {e.__str__()}")
        return False


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
