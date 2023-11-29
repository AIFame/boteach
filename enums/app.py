import logging
import os
from dataclasses import dataclass


from config import open_ai
from config.constants import INDEX_NAME, VIDEO_PATH
from utils.ai.open_ai import create_or_get_conversation_chain, upsert

import streamlit as st

from utils.inputs.get_repo import get_video_transcript


@dataclass
class App:
    """
    app: state
    """

    start_time: int = 0
    video = VIDEO_PATH

    def __post_init__(self):
        open_ai.setup()

        doc = get_video_transcript()

        logging.info(f"text_chunks are generated and the total chucks are {len(doc)}")

        # TODO: already upserted
