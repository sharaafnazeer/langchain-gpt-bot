from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
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
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-ada-002")

template = """Given the following conversation and a follow up question, rephrase the follow up question to be 
a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:
"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(template)

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the 
answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"], validate_template=False
)

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENVIRONMENT"))


def generate_content() -> None:
    from langchain.document_loaders import PyPDFLoader
    loader = PyPDFLoader(doc)
    documents = loader.load()

    # split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=os.getenv("PINECONE_INDEX"),
                        namespace="langchain-namespace",
                        batch_size=96,
                        text_key="text")


def make_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 20})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')
    model = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    chain = ConversationalRetrievalChain.from_llm(llm=model, retriever=retriever, return_source_documents=True,
                                                  verbose=True, memory=memory,
                                                  # qa_prompt=QA_PROMPT,
                                                  condense_question_prompt=CONDENSE_QUESTION_PROMPT)
    # , qa_prompt=QA_PROMPT, condense_question_prompt=CONDENSE_PROMPT

    return chain


def process_content(query, chat_history):
    vector_store = Pinecone.from_existing_index(os.getenv("PINECONE_INDEX"), embeddings, text_key="text",
                                                namespace="langchain-namespace")

    chain = make_chain(vector_store)
    result = chain({"question": query, "chat_history": chat_history})
    chain.verbose = True
    return result


def test():
    # initialize pinecone
    index = pinecone.Index('langchain-index')
    index_stats_response = index.describe_index_stats()

    print(index_stats_response)
