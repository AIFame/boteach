import logging
import time
from dataclasses import dataclass
from io import BytesIO
from typing import Final

import openai
from openai.types.beta import Thread
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

from config.constants import (
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION_ID,
    OPENAI_ASSISTANT_ID,
)
from config.log import setup_log
from enums.promptAnswer import PromptAnswer
from utils.helpers_youtube import is_valid_youtube_url

DEFAULT_VIDEO: Final = "https://www.youtube.com/watch?v=cd_KQbf-j_w"


@dataclass
class App:
    """
    app: state
    """

    start_time: int = 0
    _video: str = "https://www.youtube.com/watch?v=cd_KQbf-j_w"
    client: openai = openai
    transcript: str = ""  # TODO:

    thread: Thread = None

    assistant_id: str = OPENAI_ASSISTANT_ID  # TODO: access from config or..

    def __post_init__(self):
        setup_log()

        openai.api_key = OPENAI_API_KEY
        openai.organization = OPENAI_ORGANIZATION_ID

        client = self.client

        self.thread = client.beta.threads.create()

    @property
    def video(self) -> str:
        return self._video or DEFAULT_VIDEO

    @video.setter
    def video(self, youtube_url: str):
        if not is_valid_youtube_url(youtube_url):
            logging.warning("invalid youtube url")
            return

        self._video = youtube_url
        logging.info(f"video set:{youtube_url}")

        srt = self.get_subtitles()

        bytes_io = BytesIO(srt.encode("utf-8"))
        openai.files.create(file=bytes_io, purpose="assistants")

    def process_question(self, user_question: str) -> PromptAnswer:
        client = self.client
        thread = self.thread
        msg = client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=user_question
        )
        logging.info(f"msg:${msg}")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
            # instructions="Please answer the queries using the knowledge provided in the files.When adding other information mark it clearly as such.with a different color"
        )
        logging.info(f"run:${run}")

        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            logging.debug(f"run:${run}")

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_messages_for_run = [
            message
            for message in messages
            if message.run_id == run.id and message.role == "assistant"
        ]
        logging.info(f"assistant_msgs:{assistant_messages_for_run}")

        answer = assistant_messages_for_run[-1]

        logging.info(f"answer {answer}")

        answer_text = answer.content[0].text.value

        answer_text = answer_text.lstrip("```json")
        answer_text = answer_text.rstrip("```")

        logging.info(f"answer text {answer_text}")

        return PromptAnswer.from_json(answer_text)

    @property
    def video_id(self) -> str:
        from pytube import extract

        video_id = extract.video_id(self.video)
        return video_id

    @staticmethod
    def upload_to_openai(filepath):
        # TODO: migrate to utils/inputs
        """Upload a file to OpenAI and return its file ID."""
        with open(filepath, "rb") as file:
            response = openai.files.create(file=file.read(), purpose="assistants")
        return response.id

    def get_subtitles(self) -> str:
        transcript = YouTubeTranscriptApi.get_transcript(
            self.video_id, languages=["en"]
        )
        logging.debug(transcript[:10])

        formatter = SRTFormatter()

        return formatter.format_transcript(transcript)

    def link_chain(self, file_id: str):
        assistant_file = self.client.beta.assistants.files.create(
            assistant_id=self.assistant_id, file_id=file_id
        )
        logging.info(assistant_file)
