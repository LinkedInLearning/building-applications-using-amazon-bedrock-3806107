#Imports
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKendraRetriever
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT

#Configure streamlit app
st.set_page_config(page_title="Employee HR Bot", page_icon="📖")
st.title("📖 Employee HR Bot")

#Define the retriever
retriever = AmazonKendraRetriever(
    index_id="a72c54e4-6e0f-4d63-bd42-418d1d37c499",
    top_k=5
)

#Define model parameters
model_kwargs = {"temperature": 0, "top_k": 10, "max_tokens_to_sample": 3000}

#Configure llm
llm = Bedrock(model_id="anthropic.claude-instant-v1", model_kwargs=model_kwargs)

#Set up message history
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs, memory_key = 'chat_history', output_key='answer', return_messages=True)
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
prompt_template = PromptTemplate( 
            input_variables=[ 'context', 'chat_history', 'question'],    
            template=my_template)

#Configure the chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm, 
    retriever=retriever, 
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": prompt_template},
    memory = memory,
    condense_question_prompt=CONDENSE_QUESTION_PROMPT
)

#Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

#If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    #Messages are saved to history automatically by Langchain during run
    output = qa.invoke({'question':prompt, 'chat_history':memory.load_memory_variables({})})
    
    #display the output
    st.chat_message("ai").write(output['answer'])