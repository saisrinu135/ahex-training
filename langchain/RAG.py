from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model='gpt-3.5-turbo')


pdf = 'pdfs/speed-control.pdf'
pdf_loader = PyPDFLoader(pdf)
docs = pdf_loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)



vector_store = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db")

retriever = vector_store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 2}
)


system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('human', "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(model, prompt)
retriever_chain = create_retrieval_chain(retriever, question_answer_chain)

query = "What is the document about?"
result = retriever_chain.invoke({'input':query})
print(result)
