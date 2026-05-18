from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import os
from sqlalchemy import create_engine, text

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)
user = os.getenv("DB_USER")
password = os.getenv('DB_PASSWORD')
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
port_db = os.getenv("DB_PORT")



def criar_conexao():
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port_db}/{database}")

engine = criar_conexao()

def testar_conexao():
    try:
        conn = engine.connect()
        print("Conexão com postgresql ok.")
        conn.close()
    except Exception as e:
        print(f'Erro na conexao {e}')


testar_conexao()

def criar_tabelas(table_name: str, df: pd.DataFrame):
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'Tabela criada no banco.')

def inserir_dados(arquivos: list):
    for arquivo in arquivos:
        table_name = Path(arquivo).stem
        df = pd.read_csv(arquivo)
        criar_tabelas(table_name, df)
    print(f'Carregamento de dados realizada com sucesso.')

def database_main():
    pasta = Path(__file__).parent.parent / 'data' / 'processed'
    if not pasta.exists():
        print(f'Pasta não encontrada.')
    if not pasta.is_dir():
        print(f'Caminho não é uma pasta.')

    arquivos = list(pasta.glob('*.csv'))

    inserir_dados(arquivos)

database_main()