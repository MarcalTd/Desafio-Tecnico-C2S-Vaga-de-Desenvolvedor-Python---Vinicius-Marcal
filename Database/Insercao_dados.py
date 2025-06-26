import pandas as pd
import json
import random
import psycopg2

# Caminho do arquivo JSON
json_path = r"C:\Users\vinic\Desktop\Desafio Técnico C2S – Vaga de Desenvolvedor Python\Database\marcas_modelos_carros.json"

def data_base(df):
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="desafio",
            user="postgres",
            password="postgre"
        )
        print("Conectado com sucesso!")
        cur = conn.cursor()

        # Criar tabela se não existir
        cur.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id SERIAL PRIMARY KEY,
            marca VARCHAR(50),
            modelo VARCHAR(50),
            ano INT,
            motorizacao VARCHAR(30),
            tipo_combustivel VARCHAR(30),
            cor VARCHAR(30),
            quilometragem INT,
            numero_portas INT,
            transmissao VARCHAR(30),
            tamanho VARCHAR(30)
        );
        """)
        conn.commit()

        # Converter DataFrame em lista de tuplas para inserir
        lista_tuplas = list(df.itertuples(index=False, name=None))

        insert_query = """
        INSERT INTO veiculos (marca, modelo, ano, motorizacao, tipo_combustivel, cor, quilometragem, numero_portas, transmissao, tamanho)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.executemany(insert_query, lista_tuplas)
        conn.commit()

        print(f"{len(df)} veículos inseridos com sucesso no banco PostgreSQL!")

        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao conectar:", e)

with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

pares_base = [{"Marca": marca, "Modelo": modelo} for marca, modelos in dados.items() for modelo in modelos]

# Listas para aleatorizar demais campos
motores = ["1.0 Flex", "1.6 Flex", "1.8", "2.0 Turbo", "1.4 TSI", "3.2 Diesel"]
combustiveis = ["Gasolina", "Etanol", "Flex", "Diesel", "GNV", "Elétrico"]
cores = ["Prata", "Preto", "Branco", "Cinza", "Vermelho", "Azul", "Verde"]
transmissoes = ["Manual", "Automática", "CVT", "Automatizada"]
tamanhos = ["Compacto", "Médio", "SUV", "Pickup", "Grande"]

veiculos = []
for _ in range(100):
    base = random.choice(pares_base)
    veiculos.append({
        "marca": base["Marca"],
        "modelo": base["Modelo"],
        "ano": random.randint(2000, 2025),
        "motorizacao": random.choice(motores),
        "tipo_combustivel": random.choice(combustiveis),
        "cor": random.choice(cores),
        "quilometragem": random.randint(0, 200000),
        "numero_portas": random.choice([2, 3, 4, 5]),
        "transmissao": random.choice(transmissoes),
        "tamanho": random.choice(tamanhos)
    })

# Criar DataFrame
df = pd.DataFrame(veiculos)

# Enviar para o banco de dados
data_base(df)

