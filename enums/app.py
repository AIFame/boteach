import os
from dataclasses import dataclass

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone

from config import open_ai, pinecone
from config.constants import INDEX_NAME
from utils.ai.open_ai import create_or_get_conversation_chain

import streamlit as st


@dataclass
class App:
    start_time: int = 0
    video = os.path.join("data", "Neurons and the brain.mp4")

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
