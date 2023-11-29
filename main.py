import logging
import random

import openai
import streamlit as st

from enums.app import App

st.set_page_config(
    page_title="Boteach",
    page_icon=":books:",
)

client = openai

# sidebar() TODO: import from views/..
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
if api_key:
    openai.api_key = api_key


st.title("Botech")

app: App = st.session_state.get("app")

if not app:
    app = App()
    logging.info("creating new app instance")
    st.session_state.app = app

st.video(app.video, start_time=app.start_time)

# sidebar() TODO:

thread = client.beta.threads.create()

st.header("Q/A Genie")  # FIXME:
user_question = st.text_input("Ask a question about the video:")


if user_question:
    # handle_userinput(user_question)

    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_question
    )

    # run = client.beta.threads.runs.create(
    #     thread_id=st.session_state.thread_id,
    #     assistant_id=assistant_id,
    #     instructions="Please answer the queries using the knowledge provided in the files.When adding other information mark it clearly as such.with a different color",
    # )

    with st.spinner("LLM Processing"):
        response = app.chain({"question": user_question})

    with st.chat_message("ai", avatar="assistant"):
        chat_history_list = response["chat_history"]
        print(f"response: {response}")
        message = chat_history_list[-1].content
        print(f"message: {message}")

        st.write(message)

        st.write("Here is the video snip that should clarify your doubts")
        app.start_time = random.randint(1, 600)  # FIXME:
        st.video(app.video, start_time=app.start_time)
        



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
