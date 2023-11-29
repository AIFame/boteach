import logging

import streamlit as st

from enums.app import App

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


st.video(app.video, start_time=0)


st.header("Q/A Genie")  # FIXME:
user_question = st.text_input("Ask a question about the video:")


if user_question:
    with st.spinner("LLM Processing"):
        response = app.process_question(user_question)

        with st.chat_message("ai", avatar="assistant"):
            st.markdown(response.answer)

        st.video(app.video, start_time=0)
