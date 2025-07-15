import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

# Implement langsmith tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Simple Q & A Chatbot with openAI'

# Define prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ('system','You are a William Shakespeare. please response to user query in a way that William Shakespeare whould have answered'),
        ('user','Question:{question}')
    ]
)


def generate_response(question, api_key, llm_name, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm_name, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer



# Creat the Streamlit app


# Title
st.title('Questions and Answers Chatbot with OpenAI')

# Create side bar
st.sidebar.title('Settings')
api_key = st.sidebar.text_input('Enter your OpenAI API KEY: ', type='password')

# Create dropdown to select OpenAI Models
llm = st.sidebar.selectbox("Select an OpenAI model", ['gpt-4o', 'gpt-4-turbo', 'gpt-4'])

# Set temperature (closer to 1 = more creative, closer to 0 = more predictable)
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7)

# Set tokens
max_tokens = st.sidebar.slider('Max Tokens', min_value=50, max_value=300, value=150)


# Main interface for user input
st.write('GO ahead and ask any question')
user_input = st.text_input('You:')


if user_input:
    response = generate_response(question=user_input,
                                 api_key=api_key,
                                 llm_name=llm,
                                 temperature=temperature,
                                 max_tokens=max_tokens)
    st.write(response)
else:
    st.write('Please Enter your query')