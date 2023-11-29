import streamlit as st
from icecream import ic

from config.constants import VIDEO_PATH
from database.pinecone_db import need_text_embedding
from utils.ai.open_ai import get_text_chunk, upsert
from utils.inputs.get_video_transcript import get_video_transcript


def sidebar_spinner():
    with st.spinner("Processing"):
        if not need_text_embedding():
            st.write(
                "Index existed in Pinecone database. Skip text embedding. You can ask question directly.",
            )
            return

        st.write("Index didn't found. Will process Embeding for you.")
        doc = get_video_transcript()

        ic(f"text_chunks are generated and the total chucks are {len(doc)}")

        print("Doc is ready for upsert!")
        upsert(doc)
        st.write(
            "Text embedding finished successfully. You can ask question now.",
        )


def sidebar():
    with st.sidebar:
        st.subheader("Process the video")

        st.write(
            "For now we only support the video displayed, We plan on extending the support to all youtube videos",
        )

        if need_text_embedding():
            st.write(
                "For brand new vector database, press Process to do text embedding first.:tada:",
            )

            # if the button is pressed
            if st.button("Text Embedding"):
                sidebar_spinner()
