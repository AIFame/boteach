import logging

import streamlit as st
from langchain.embeddings import OpenAIEmbeddings

from enums.app import App
from public import tpl_bot

st.set_page_config(
    page_title="Boteach",
    page_icon=":books:",
)

st.title("Botech")

app: App = st.session_state.get("app")

if not app:
    app = App()
    logging.info("creating new app instance")
    st.session_state.app = app

st.video(app.video, start_time=app.start_time)

# sidebar() TODO:

if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.header(" Q/A assistant for slow learners")
user_question = st.text_input("Ask a question about the video:")

if user_question:
    # handle_userinput(user_question)
    response = app.chain({"question": user_question})
    chat_history_list = response["chat_history"]
    print(f"response: {response}")
    message = chat_history_list[-1].content
    print(f"message: {message}")
    st.write(
        tpl_bot.replace(
            "{{MSG}}",
            message,
        ),
        unsafe_allow_html=True,
    )

    OpenAIEmbeddings()


# Define a function to answer a question about a video
# def answer_question(question, video_url):
#     # Get the video snip of the explanation
#     video_snip =
#
#     # Answer the question using the QA model
#     answer = qa_model.answer(question, video_snip)
#
#     # Return the answer and the video snip
#     return answer, video_snip


# Set the title of the app

# Display the video

# Ask the user a question about the video

# Answer the question and display the video snip
# if question:
#     answer, video_snip = answer_question(question, video_url)
#
#     st.write(answer)
#     st.image(video_snip)
