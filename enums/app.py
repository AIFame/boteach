import logging
import time
from dataclasses import dataclass
from typing import List

import openai
from dataclasses_json import dataclass_json, LetterCase
from openai.types.beta import Thread

from config.constants import (
    VIDEO_PATH,
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION_ID,
    OPENAI_ASSISTANT_ID,
)
from config.log import setup_log


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PromptAnswer:
    video_timestamps: List[str]
    answer: str


@dataclass
class App:
    """
    app: state
    """

    start_time: int = 0
    video = VIDEO_PATH
    client: openai = openai
    transcript: str = ""

    thread: Thread = None

    assistant_id: str = OPENAI_ASSISTANT_ID  # TODO: access from config or..

    def __post_init__(self):
        setup_log()

        openai.api_key = OPENAI_API_KEY
        openai.organization = OPENAI_ORGANIZATION_ID

        client = self.client

        self.thread = client.beta.threads.create()

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

        answer = assistant_messages_for_run[-1].content

        logging.info(f"answer {answer}")

        return PromptAnswer.from_json(answer)

    @staticmethod
    def upload_to_openai(filepath):
        # TODO: migrate to utils/inputs
        """Upload a file to OpenAI and return its file ID."""
        with open(filepath, "rb") as file:
            response = openai.files.create(file=file.read(), purpose="assistants")
        return response.id
