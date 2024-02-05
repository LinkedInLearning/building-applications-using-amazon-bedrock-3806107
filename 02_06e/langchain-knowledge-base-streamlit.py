#Imports
from langchain.chains import RetrievalQA
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts.prompt import PromptTemplate

#Configure streamlit app
st.set_page_config(page_title="Employee HR Bot")
st.title("Employee HR Bot")

#Define the retriever
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)

#Define model parameters
model_kwargs_claude = {
  "temperature" : 0,
  "top_k" : 10,
  "max_tokens_to_sample" : 750
}

#Configure llm
llm = Bedrock(model_id="anthropic.claude-instant-v1", model_kwargs=model_kwargs_claude)

#Set up message history
msgs = StreamlitChatMessageHistory(key = "langchain_messages")
memory = ConversationBufferMemory(chat_memory = msgs, memory_key='history', ai_prefix='Assistant', output_key='answer')
if len(msgs.messages) == 0:
  msgs.add_ai_message("How can I help you?")

#Creating the template   
my_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. 
{context}
Question: {question}
Helpful Answer:"""  

#Configure prompt template

#Configure the chain

#Render current messages from StreamlitChatMessageHistory

#If user inputs a new prompt, generate and draw a new response
