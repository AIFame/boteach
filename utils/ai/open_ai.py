from icecream import ic
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.base import (
    BaseConversationalRetrievalChain,
)
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from config.constants import INDEX_NAME, OPENAI_CHAT_MODEL, OPENAI_EMBEDDINGS_LLM
from database import pinecone_db
from utils.inputs.get_repo import get_github_docs, get_video_transcript


def upsert(data) -> Pinecone:
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDINGS_LLM)

    #   will not to use vector in memory today.
    #    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    pinecone_db.create_index(INDEX_NAME)
    # to get more information, you can look at this page
    # https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/pinecone

    vectorstore = pinecone_db.insert(
        data,
        embeddings,
    )
    return vectorstore


def get_text_chunk(text):
    # use text_splitter to split it into documents list
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )
    chunks = text_splitter.split_text(text)

    # (variable) docs: List[Document]
    docs = [Document(page_content=text) for text in chunks]
    return docs


def create_or_get_conversation_chain(vectorstore):
    template = """
        Return results as markdown code?
    """
    # llm = ChatOpenAI(model=OPENAI_CHAT_MODEL)
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )
    prompt_template = PromptTemplate.from_template(template)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        condense_question_prompt=prompt_template,
    )
    # ic(f'conversation_chain is {conversation_chain}')
    return conversation_chain
