#Imports
from langchain.chains import RetrievalQA
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

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
memory = ""
if len(msgs.messages) == 0:
  msgs.add_ai_message("How can I help you?")

#Creating the template   
my_template = """
Human: 
    You are a conversational assistant designed to help answer questions from a knowledge base. 
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. 

{context}

{chat_history}

Question: {question}

Assistant:
"""

#configure prompt template
prompt_template = ""

#Configure the chain
qa = ""

#Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
  st.chat_message(msg.type).write(msg.content)

#If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
  st.chat_message("human").write(prompt)

  #Invoke the model
  output = ""
    
  #display the output
  st.chat_message("ai").write(output['answer'])  