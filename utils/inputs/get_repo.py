import logging
import pathlib
import subprocess
import tempfile

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.constants import VIDEO_PATH, VIDEO_TRANSCRIPT_PATH


def get_text_chunk(text) -> [Document]:
    # use text_splitter to split it into documents list
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )
    chunks = text_splitter.split_text(text)

    # (variable) docs: List[Document]
    docs = [Document(page_content=text) for text in chunks]
    return docs


def get_video_transcript(transcript: str = VIDEO_TRANSCRIPT_PATH) -> [Document]:
    with open(transcript, "r") as f1:
        docs = get_text_chunk(f1.read())
        return docs
        # return Document(page_content=f1.read(), metadata={"source": VIDEO_PATH})
