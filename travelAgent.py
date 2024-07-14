import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

import bs4


llm = ChatOpenAI(model='gpt-3.5-turbo')

query = """
    Vou viajar para Londres em agosto de 2024. Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com o preço da passagem do Rio de Janeiro para Londres.
"""


def research_agent(query, llm):
    # Ferramentas
    tools = load_tools(['ddg-search', 'wikipedia'], llm=llm)
    # Prompt
    prompt = hub.pull('hwchase17/react')
    # Criação do agente react (Reason + Act)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt, verbose=True)
    webContext = agent_executor.invoke({'input': query})
    return webContext['output']

def loadData():
    loader = WebBaseLoader(
        webpaths=("https://www.dicasdeviagem.com/inglaterra/"),
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("postcontentwrap", "pagetitleloading background-imaged loading-dark")))
    )
    docs = loader.load()

    # Separando o texto em chunks menores
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Salvando no banco de dados vetorial Chroma
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings)
    retriever = vectorstore.as_retriever()
    return retriever
