from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

# loading environment variables
load_dotenv()

# initializing a chat model
model = ChatOpenAI(model='gpt-3.5-turbo')

# initializing a output parser
parser = StrOutputParser()

#messages
messages = [
    ('system', 'You are a standup comedian in {language}'),
    ('human', 'Tell me a joke on {topic}')
]

# making propmts
propmt = ChatPromptTemplate.from_messages(messages)



# initializing a runnalble (runnables are just like small tasks)
make_propmt = RunnableLambda(lambda x: propmt.format_messages(**x))
invoke_model = RunnableLambda(lambda x: model.invoke(x))
parse_output = RunnableLambda(lambda x: x.content)


# connecting runnables (runnables sequence is sequence os tasks)
chain = RunnableSequence(first=make_propmt, middle=[invoke_model], last=parse_output)


# invoking tha chain
response = chain.invoke({'language': 'English', 'topic': 'office'})

# printing the response
print(response)