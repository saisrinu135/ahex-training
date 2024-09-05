from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough

# load from environment variables
load_dotenv()

model = ChatOpenAI(model='gpt-4')
parser = StrOutputParser()

store = {}


# using sessions to get past chat objects
def get_session_history_chat(session_id :str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chain = model | parser

chat_with_history = RunnableWithMessageHistory(chain, get_session_history_chat)
# defining the session id
config = {"configurable": {"session_id": "abc2"}}

result = chat_with_history.invoke(
    [
        HumanMessage("What is my name")
    ],
    config=config
)

print(result)
# print(store)