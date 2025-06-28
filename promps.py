import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


chave_api = os.getenv("OPENAI_API_KEY")  # Nome da variável, não o caminho do arquivo

# Inicializar modelo com a chave explícita
modelo = ChatOpenAI(api_key=chave_api, model="gpt-4o")
parser = StrOutputParser()

# Função para gerar SQL
def gerar_sql(historico, pergunta):
    mensagens = [
        SystemMessage(content="Gere apenas o comando SQL para pesquisar na tabela 'veiculos'. Não explique nem use markdown. Use ILIKE em todas comparações de strings para ignorar maiúsculas/minúsculas."),
        HumanMessage(content=pergunta)
    ] + historico
    resposta = modelo.invoke(mensagens)
    return parser.invoke(resposta).strip()

# Função para interpretar o resultado do banco
def interpretar_resultado(resultado_bruto):
    mensagens = [
        SystemMessage(content="Você é um atendente de concessionária. Interprete os dados recebidos do banco e gere uma resposta amigável e clara para o cliente."),
        HumanMessage(content=f"Resultado da busca:\n{resultado_bruto}")
    ]
    resposta = modelo.invoke(mensagens)
    return parser.invoke(resposta).strip()

# Função para detectar fim da conversa
def verificar_encerramento_conversa(pergunta_usuario):
    mensagens = [
        SystemMessage(content="Você é um assistente que detecta se o usuário quer encerrar a conversa."),
        HumanMessage(content=f"Esta frase indica que o usuário quer encerrar a conversa? Responda apenas com 'sim' ou 'não'.\n\nFrase: \"{pergunta_usuario}\"")
    ]
    resposta = modelo.invoke(mensagens)
    decisao = parser.invoke(resposta).strip().lower()
    return decisao.startswith("s")
