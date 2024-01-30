#Imports
from langchain.chains import RetrievalQA
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts.prompt import PromptTemplate

#Configure streamlit app
st.set_page_config(page_title="Employee HR Bot", page_icon="📖")
st.title("📖 Employee HR Bot")

#Define the retriever
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="P4P5UVX2UB",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)

#Define model parameters
model_kwargs_claude = {"temperature": 0, "top_k": 10, "max_tokens_to_sample": 3000}

#Configure llm
llm = Bedrock(model_id="anthropic.claude-instant-v1", model_kwargs=model_kwargs_claude)


#Set up message history
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs, memory_key = 'history', ai_prefix='Assistant', output_key='answer')
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

#Creating the template   
my_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. 
{context}
Question: {question}
Helpful Answer:"""

#Configure prompt template
prompt_template= PromptTemplate.from_template(my_template)

#Configure the chain
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff",
    retriever=retriever, 
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

#Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

#If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    #Messages are saved to history automatically by Langchain during run
    output = qa.invoke({'query':prompt})
    
    #adding messages to memory
    memory.chat_memory.add_user_message(prompt)
    memory.chat_memory.add_ai_message(output['result'])
    
    #display the output
    st.chat_message("ai").write(output['result'])    