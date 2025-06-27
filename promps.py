import os
import socket
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

# Inicializar modelo e parser
modelo = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()


def gerar_sql(historico,pergunta):
    mensagens = [
        SystemMessage(content="Gere apenas o comando SQL para pesquisar na tabela 'veiculos'. Não explique nem use markdown. Use ILIKE em todas comparações de strings para ignorar maiúsculas/minúsculas."),
        HumanMessage(content=pergunta)
    ] + historico
    resposta = modelo.invoke(mensagens)
    return parser.invoke(resposta).strip()

def interpretar_resultado(resultado_bruto):
    mensagens = [
        SystemMessage(content="Você é um atendente de concessionária. Interprete os dados recebidos do banco e gere uma resposta amigável e clara para o cliente."),
        HumanMessage(content=f"Resultado da busca:\n{resultado_bruto}")
    ]
    resposta = modelo.invoke(mensagens)
    return parser.invoke(resposta).strip()

def verificar_encerramento_conversa(pergunta_usuario):
    mensagens = [
        SystemMessage(content="Você é um assistente que detecta se o usuário quer encerrar a conversa."),
        HumanMessage(content=f"Esta frase indica que o usuário quer encerrar a conversa? Responda apenas com 'sim' ou 'não'.\n\nFrase: \"{pergunta_usuario}\"")
    ]
    resposta = modelo.invoke(mensagens)
    decisao = parser.invoke(resposta).strip().lower()
    return decisao.startswith("s")