#Imports
from langchain.chains import RetrievalQA
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever

#Define the retriever
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="P4P5UVX2UB",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)

#Define model parameters
model_kwargs_claude = {"temperature": 0, "top_k": 10, "max_tokens_to_sample": 750}

#Configure llm
llm = Bedrock(model_id="anthropic.claude-instant-v1", model_kwargs=model_kwargs_claude)

#Configure the chain
qa = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, return_source_documents=True
)

#Get user input and display the result
while True:
    query = input("\nAsk a question:\n")

    #invoke the model
    output = qa.invoke(query)

    #display the output
    print (output['result'])