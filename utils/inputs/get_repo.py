import logging
import pathlib
import subprocess
import tempfile

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.constants import VIDEO_PATH


def get_github_docs(repo_owner, repo_name):
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(
            f"git clone --depth 1 https://github.com/{repo_owner}/{repo_name}.git .",
            cwd=d,
            shell=True,
        )
        git_sha = (
            subprocess.check_output("git rev-parse HEAD", shell=True, cwd=d)
            .decode("utf-8")
            .strip()
        )
        repo_path = pathlib.Path(d)
        markdown_files = list(repo_path.glob("*/*.md")) + list(
            repo_path.glob("*/*.mdx"),
        )
        for markdown_file in markdown_files:
            with open(markdown_file) as f:
                relative_path = markdown_file.relative_to(repo_path)
                github_url = f"https://github.com/{repo_owner}/{repo_name}/blob/{git_sha}/{relative_path}"
                yield Document(page_content=f.read(), metadata={"source": github_url})


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


def get_video_transcript() -> [Document]:
    with open(VIDEO_PATH, "r") as f1:
        docs = get_text_chunk(f1.read())
        return docs
        # return Document(page_content=f1.read(), metadata={"source": VIDEO_PATH})
