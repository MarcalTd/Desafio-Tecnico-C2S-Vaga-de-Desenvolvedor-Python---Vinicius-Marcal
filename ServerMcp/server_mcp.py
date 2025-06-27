import socket

import psycopg2


def start_server():
    HOST = 'localhost'
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor MCP rodando em {HOST}:{PORT}")

        while True:
            conn_client, addr = s.accept()
            with conn_client:
                print(f"Conexão de {addr}")
                sql_query = conn_client.recv(8192).decode()
                print(f"SQL original recebido:\n{sql_query}")

                # Limpar tags markdown do SQL
                sql_query = sql_query.strip()
                if sql_query.startswith("```sql"):
                    sql_query = sql_query[len("```sql"):]

                if sql_query.endswith("```"):
                    sql_query = sql_query[:-3]

                sql_query = sql_query.strip()
                print(f"SQL limpo para execução:\n{sql_query}")

                try:
                    conn_db = psycopg2.connect(
                        host="localhost",
                        port=5432,
                        database="desafio",
                        user="postgres",
                        password="postgre"
                    )
                    cur = conn_db.cursor()
                    cur.execute(sql_query)
                    resultados = cur.fetchall()

                    resposta = ""
                    for linha in resultados:
                        resposta += str(linha) + "\n"

                    if not resposta:
                        resposta = "Nenhum resultado encontrado."

                    cur.close()
                    conn_db.commit()
                    conn_db.close()

                    conn_client.sendall(resposta.encode())

                except Exception as e:
                    erro_str = f"Erro ao executar SQL: {str(e)}"
                    conn_client.sendall(erro_str.encode())


if __name__ == "__main__":
    start_server()
