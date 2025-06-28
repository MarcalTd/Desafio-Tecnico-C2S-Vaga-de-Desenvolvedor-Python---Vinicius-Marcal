import socket

import psycopg2


def parse_mcp_request(request: str):
    """Faz o parsing de uma requisição MCP"""
    lines = request.split("\n")
    if not lines[0].startswith("MCP/1.0"):
        raise ValueError("Protocolo inválido")

    command = None
    length = 0
    body_index = 0

    for i, line in enumerate(lines[1:], 1):
        if line.startswith("COMMAND:"):
            command = line.split(":", 1)[1].strip()
        elif line.startswith("LENGTH:"):
            length = int(line.split(":", 1)[1].strip())
        elif line.strip() == "":
            body_index = i + 1
            break

    body = "\n".join(lines[body_index:])
    if len(body.encode()) != length:
        raise ValueError("Comprimento do corpo inválido")

    return command, body

def build_mcp_response(status: str, body: str):
    body_bytes = body.encode()
    return f"MCP/1.0\nSTATUS: {status}\nLENGTH: {len(body_bytes)}\n\n{body}"

def handle_query(sql_query: str):
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

        try:
            resultados = cur.fetchall()
            resposta = "\n".join(str(row) for row in resultados)
        except psycopg2.ProgrammingError:
            resposta = "Comando executado com sucesso."

        cur.close()
        conn_db.commit()
        conn_db.close()

        return "OK", resposta or "Nenhum resultado encontrado."
    except Exception as e:
        return "ERROR", f"Erro ao executar SQL: {str(e)}"

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
                print(f"\nConexão de {addr}")
                data = conn_client.recv(8192).decode()
                print(f"Requisição MCP recebida:\n{data}")

                try:
                    command, body = parse_mcp_request(data)
                    print(f"Comando: {command}")
                    if command == "QUERY":
                        status, result = handle_query(body)
                    else:
                        status, result = "ERROR", f"Comando desconhecido: {command}"
                except Exception as e:
                    status, result = "ERROR", f"Erro no protocolo: {str(e)}"

                response = build_mcp_response(status, result)
                conn_client.sendall(response.encode())

if __name__ == "__main__":
    start_server()
