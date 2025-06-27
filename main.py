import os
import socket
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Carregar variáveis de ambiente
load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

# Inicializar modelo e parser
modelo = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()

# Saudação automática
hora = datetime.now().hour
if 5 <= hora < 13:
    saudacao = "Bom dia"
elif 13 <= hora < 18:
    saudacao = "Boa tarde"
else:
    saudacao = "Boa noite"

print(f"chat_bot: {saudacao}! Em que posso ajudar na sua busca por veículos?")

# Histórico da conversa
historico = []

def gerar_sql(historico):
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

# Loop principal de interação
while True:
    pergunta = input("humano: ")

    if verificar_encerramento_conversa(pergunta):
        print("chat_bot: Foi um prazer te ajudar! Até a próxima.")
        break

    # Adicionar a pergunta ao histórico
    historico.append(HumanMessage(content=pergunta))

    # Gerar SQL com contexto
    sql = gerar_sql(historico)
    print("chat_bot: Comando SQL gerado:", sql)

    # Enviar SQL ao servidor MCP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5000))
            s.sendall(sql.encode())
            resposta_raw = s.recv(16384).decode()
    except Exception as e:
        print("chat_bot: Não consegui consultar os dados. O servidor está online?")
        continue

    # Interpretar resposta
    try:
        resposta_humana = interpretar_resultado(resposta_raw)
        print("chat_bot:", resposta_humana)
        historico.append(AIMessage(content=resposta_humana))
    except Exception as e:
        print("chat_bot: Ocorreu um erro ao interpretar os dados:", str(e))