# NLW Journey Trilha IA
 NLW Journey Trilha IA da Rocketseat

# Desafio
    Através de uma aplicação própria, utilizar o modelo do chatGPT, o GPT, através de API para geração de texto na aplicação, dando mais contexto e fornecendo uma solução mais completa, respondendo uma resposta de forma mais detalhada, possibilitando que o agente de viagens use o langchain para integrar com o modelo do gpt e esse modelo utilizar ferramentas do duckduckgo search e wikipedia para fazer pesquisas na internet. Além disso, foi adicionado documentos do site dicasdeviagem.com para o modelo utilizar e trazer ainda mais informações.
    Foi criado um agente que realiza as buscas na internet e outro agente supervisor para revisar os resultados do agente de pesquisa, compilando as respostas dos agentes e retornando uma mensagem final.
    Para pegar o conteúdo do site dicasdeviagem.com, foi transformado o conteudo em embed (informação numérica) e foi salvo em um banco de dados vetorial (RAG).

# Requisitos
    É necessário ter uma KEY da OpenAI, no terminal digitar: export OPENAI_API_KEY="SUA_KEY"

# Bibliotecas
    - openai
    - langchain
    - duckduckgo-search
    - wikipedia
    - beautifulsoup4

# Banco de dados vetorial
    - LangChain Chroma

# Site API GPT
platform.openai.com/playground

# Deploy
    - Docker:
        - Criação do docker file
        - docker build --platform linux/x86_64 -t travelagent .
    - AWS Cloud
        - Amazon Elastic Container Registry: Registro da AWS (Versionamento, Gestão)
        - IAM: Controle de usuário
        - Lambda Function: Código como Serviço (Serverless Function)
        - EC2: API DNS