import os
from dataclasses import dataclass

from icecream import ic
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone

from config import open_ai, pinecone
from config.constants import INDEX_NAME, VIDEO_PATH
from utils.ai.open_ai import create_or_get_conversation_chain, upsert

import streamlit as st

from utils.inputs.get_repo import get_video_transcript


@dataclass
class App:
    start_time: int = 0
    video = VIDEO_PATH

    def __post_init__(self):
        open_ai.setup()
        pinecone.setup()

        embeddings = OpenAIEmbeddings()
        vectorstore = Pinecone.from_existing_index(
            index_name=INDEX_NAME,
            embedding=embeddings,
        )

        st.session_state.conversation = create_or_get_conversation_chain(
            vectorstore,
        )

        doc = get_video_transcript()

        ic(f"text_chunks are generated and the total chucks are {len(doc)}")

        print("Doc is ready for upsert!")
        upsert(doc)
