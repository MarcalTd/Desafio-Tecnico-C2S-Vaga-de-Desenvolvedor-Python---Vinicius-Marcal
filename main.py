import os
import socket
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# from comando_voz import ouvir_comando
from promps import (gerar_sql, interpretar_resultado,
                    verificar_encerramento_conversa)

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



while True:
    pergunta = input("humano: ")

    if verificar_encerramento_conversa(pergunta):
        print("chat_bot: Foi um prazer te ajudar! Até a próxima.")
        break

    # Adicionar a pergunta ao histórico
    historico.append(HumanMessage(content=pergunta))

    sql = gerar_sql(historico,pergunta)
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