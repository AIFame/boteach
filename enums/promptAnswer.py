from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PromptAnswer:
    answer: str
    start_video_timestamp: str
    end_video_timestamp: str

    @staticmethod
    def timestamp_to_seconds(timestamp) -> int:
        h, m, s = map(float, timestamp.split(":"))
        return int(h * 3600 + m * 60 + s)

    @property
    def start_time(self):
        return self.timestamp_to_seconds(self.start_video_timestamp)

    @property
    def end_time(self):
        return self.timestamp_to_seconds(self.end_video_timestamp)
