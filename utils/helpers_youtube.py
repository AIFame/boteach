import logging

from pytube import YouTube


def is_valid_youtube_url(url):
    try:
        YouTube(url)
        return True
    except Exception as e:
        logging.exception(f"youtube url {e.__str__()}")
        return False
