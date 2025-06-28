Chatbot SQL com OpenAI e PostgreSQL
===================================

Este projeto implementa uma arquitetura Client ↔ Server ↔ Banco de Dados, onde o cliente (usuário via terminal) se comunica com um chatbot inteligente. Esse chatbot traduz comandos em linguagem natural para SQL, envia-os a um servidor, que por sua vez executa essas queries em um banco PostgreSQL e retorna os resultados para o cliente.

-----------------------------------
INSTRUÇÕES DE EXECUÇÃO
-----------------------------------

1. Preparar o Banco de Dados
----------------------------
- Crie a base de dados chamada "desafio" no PostgreSQL.
- Em seguida, execute o script:

    cd Database
    python Insercao_dados.py

Esse script vai popular o banco com modelos e marcas de carros a partir do arquivo marcas_modelos_carros.json.

2. Configurar o Servidor
-------------------------
- Abra o arquivo "Server MCP/server_mcp.py"
- Altere os parâmetros da conexão PostgreSQL, se necessário:

    conn_db = psycopg2.connect(
        host="localhost",
        port=5432,
        database="desafio",
        user="seu_usuario",
        password="sua_senha"
    )

- Execute o servidor:

    cd Server MCP
    python server_mcp.py

O servidor ficará escutando requisições SQL na porta 5000.

3. Configurar a API da OpenAI
-----------------------------
- Na pasta raiz do projeto, crie um arquivo chamado ".env" com o seguinte conteúdo:

    OPENAI_API_KEY="sua-chave-da-openai"

Você pode obter sua chave em: https://platform.openai.com/account/api-keys

4. Executar o Cliente Chatbot
-----------------------------
- Na pasta raiz do projeto, execute:

    python main.py

Você poderá interagir via terminal com o chatbot, fazendo perguntas como:

- Quais são os modelos da marca Honda?
- Quantas marcas de carro existem?
- Me mostra todos os modelos que começam com a letra F

O arquivo promps.py contém os prompts base usados pelo chatbot.

-----------------------------------
RECURSO OPCIONAL: COMANDO DE VOZ
-----------------------------------

Este projeto também possui uma funcionalidade opcional de comando de voz.

Para ativá-la:

1. Descomente a **linha 10** do arquivo `main.py`:

    from comando_voz import ouvir_comando

2. Substitua a variável `pergunta = input(...)` na **linha 30** por:

    pergunta = ouvir_comando()

Certifique-se de que seu microfone está funcionando corretamente e que todas as dependências necessárias para captura de áudio estejam instaladas (como `speech_recognition` e `pyaudio`).

-----------------------------------
ESTRUTURA DO SISTEMA
-----------------------------------

Client (main.py)
   ↓           - Gera SQL com ChatGPT
< Server (server_mcp.py) >
   ↓           - Executa SQL no PostgreSQL
< Banco de Dados (desafio) >

-----------------------------------
REQUISITOS
-----------------------------------

- Python 3.8+
- PostgreSQL rodando localmente

Pacotes Python (requirements.txt):

    openai
    langchain
    langchain-openai
    python-dotenv
    psycopg2-binary
    pandas

Instale com:

    pip install -r requirements.txt

-----------------------------------
DESAFIO TÉCNICO
-----------------------------------

Este projeto foi desenvolvido como parte de um DESAFIO TÉCNICO para a vaga de Desenvolvedor Python na empresa **Contact2Sale (C2S)**.

-----------------------------------
📚 REFERÊNCIAS
-----------------------------------

🔹 LangChain (Documentação oficial):  
https://python.langchain.com/

🔹 OpenAI API (Docs + Chaves de API):  
https://platform.openai.com/docs

