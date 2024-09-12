from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from langchain_chroma import Chroma


from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# initialing a chat model
model = ChatOpenAI(model='gpt-4')

# output parser
parser = StrOutputParser()

# define the directories for current, file, and the database
curr_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(curr_dir, 'pdfs', 'speed-control.pdf')
persistant_dir = os.path.join(curr_dir, 'chroma_db')


#Check if the vector database exists
if not os.path.exists(persistant_dir):
    print("\nDatabase not found. Creating one")

    # checks if the file exixts
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file {file_path} not found")
    
    # loading the document
    print("\nLoading document")
    loader = PyPDFLoader(file_path)
    docs = loader.load()


    # splitting the document into chunks
    print("\nSplitting document into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    print(f"Document is splitted into {len(splits)} parts")

    # Creating a vector store out of chunks
    print("\nCreating a vector store")
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory=persistant_dir
    )
    print("\nDatabase created")

else:
    print("\nDatabase found. Need not to initialize")


#vectore store
vector_store = Chroma(
    persist_directory=persistant_dir,
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
    )

# initializing a retriever
print("Creatig retriever")
retreiver = vector_store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 2}
    
)

# taking query
query = "What is BLDC Motor? and How it is different from Traditional DC motor?"

# retriveing documents
print("Retrieving related documents")
documents = retreiver.invoke(query)

combined_input = f"""Here are the documents relatd to the query:
                {query}
                Relevant documents:
                {"".join([doc.page_content for doc in documents])}
                Please provide the answer based on the provided documents. If the answer is not there in documents reply with 'I don't know'
                """

# creates chain
chain = model | parser

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content=combined_input)
]

# invoking chain
response = chain.invoke(messages)

# printing the response
print(response)


