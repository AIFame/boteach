import logging
import os
from dataclasses import dataclass


from config import open_ai
from config.constants import INDEX_NAME, VIDEO_PATH

import streamlit as st


@dataclass
class App:
    """
    app: state
    """

    start_time: int = 0
    video = VIDEO_PATH

    def __post_init__(self):
        open_ai.setup()

        # TODO: upload transcript
        # TODO: already upserted
