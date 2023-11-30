import logging

import streamlit as st
from pytube import YouTube

from enums.app import App


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


# sidebar() TODO: import from views/..
# st.sidebar.header("Configuration")
# api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
# if api_key:
#     openai.api_key = api_key


st.title("Botech")

app: App = st.session_state.get("app")
app = None  # FIXME
if not app:
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


if user_question:
    with st.spinner("LLM Processing"):
        response = app.process_question(user_question)

        with st.chat_message("ai", avatar="assistant"):
            st.markdown(response.answer)

        st.video(app.video, start_time=response.start_time)
