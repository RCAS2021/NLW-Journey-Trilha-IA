import os
import bs4
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain.agents import create_react_agent, AgentExecutor
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence


llm = ChatOpenAI(model='gpt-3.5-turbo')

def research_agent(query, llm):
    # Ferramentas
    tools = load_tools(['ddg-search', 'wikipedia'], llm=llm)
    # Prompt
    prompt = hub.pull('hwchase17/react')
    # Criação do agente react (Reason + Act)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt, verbose=False)
    webContext = agent_executor.invoke({'input': query})
    return webContext['output']

def loadData():
    loader = WebBaseLoader(
        web_paths=("https://www.dicasdeviagem.com/inglaterra/"),
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

def getRelevantDocs(query):
    retriever = loadData()
    relevant_documents = retriever.invoke(query)
    #print(relevant_documents)
    return relevant_documents

def supervisorAgent(query, llm, webContext, relevant_documents):
    prompt_template = """
    Você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagens completo e detalhado.
    Utilize o contexto de eventos e preços de passagens, o input do usuário e também os documentos relevantes para elaborar o roteiro.

    Contexto: {webContext}
    Documentos relevantes: {relevant_documents}
    Usuário: {query}
    Assistente:
    """ 
    prompt = PromptTemplate(
        input_variables=['webContext', 'relevant_documents', 'query'],
        template=prompt_template
    )

    sequence = RunnableSequence(prompt | llm)

    response = sequence.invoke({"webContext": webContext, "relevant_documents": relevant_documents, "query": query})

    return response

def getResponse(query, llm):
    webContext = research_agent(query, llm)
    relevant_documents = getRelevantDocs(query)
    response = supervisorAgent(query, llm, webContext, relevant_documents)
    return response

def lambda_handler(event, context):
    query = event.get("question")
    response = getResponse(query, llm).content
    return {"body": response, "status": 200}