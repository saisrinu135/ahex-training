from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables (e.g., API keys)
load_dotenv()

# Initialize ChatGPT model
chat_model = ChatOpenAI(model='gpt-3.5-turbo')

# Initialize string output parser
string_parser = StrOutputParser()

# Define conversation template for joke generation
joke_template = [
    ('system', 'You are a standup comedian in {language}'),
    ('human', 'Tell me a joke about {topic}')
]

# Create chat prompt template
joke_prompt = ChatPromptTemplate.from_messages(joke_template)

# Define individual runnables (tasks)
format_prompt = RunnableLambda(lambda inputs: joke_prompt.format_messages(**inputs))
generate_response = RunnableLambda(lambda messages: chat_model.invoke(messages))
extract_content = RunnableLambda(lambda model_output: model_output.content)

# Create a sequence of runnables for joke generation
joke_generator = RunnableSequence(
    first=format_prompt,
    middle=[generate_response],
    last=extract_content
)

# Generate a joke with specific language and topic
generated_joke = joke_generator.invoke({'language': 'English', 'topic': 'office'})

# Display the generated joke
print(generated_joke)