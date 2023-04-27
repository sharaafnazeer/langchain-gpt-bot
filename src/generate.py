from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.memory import ConversationBufferMemory
import pinecone

import os
from dotenv import load_dotenv

load_dotenv()
cwd = os.getcwd()
doc = cwd + '/docs/Book.pdf'

# select which embeddings we want to use
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENVIRONMENT"))


def generate_content() -> None:
    from langchain.document_loaders import PyPDFLoader
    loader = PyPDFLoader(doc)
    documents = loader.load()

    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # initialize pinecone

    Pinecone.from_documents(texts, embeddings, index_name="langchain-index", namespace="langchain-namespace",
                            text_key="text")


def make_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')
    model = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    chain = ConversationalRetrievalChain.from_llm(llm=model, retriever=retriever, return_source_documents=True,
                                                  verbose=True)
    # , qa_prompt=QA_PROMPT, condense_question_prompt=CONDENSE_PROMPT

    return chain


def process_content(query, chat_history):
    vector_store = Pinecone.from_existing_index("langchain-index", embeddings, text_key="text",
                                                namespace="langchain-namespace")

    chain = make_chain(vector_store)
    result = chain({"question": query, "chat_history": chat_history})
    return result
