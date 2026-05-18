import pandas as pd
from pathlib import Path
from nba_api.stats.endpoints import leagueleaders
import time
import json
 
path_name = Path(__file__).parent.parent / 'data' / 'raw' / 'nba_players.csv'
coluns_rename = {'PLAYER':'JOGADOR',
                    'TEAM_ID': 'TIME_ID',
                    'PLAYER_ID':'JOGADOR_ID',
                    'TEAM': 'TIME',
                    'GP':'JOGOS_JOGADOS',
                    'MIN':'MINUTOS',
                    'PF':'FALTAS',
                    'EFF': 'EFICIENCIA',
                    'temporada': 'TEMPORADA',
                    'categoria': 'CATEGORIA'}

def create_dataframe(path_name:str) -> pd.DataFrame:
    print(f'Criando DataFrame do arquivo csv.')
    path = Path(path_name)

    if not path.exists():
        print(f'Arquivo não encontrado')
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    print(f'Dataframe criado. Com {len(df)} linhas')
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:

    df_players = df.rename(columns= coluns_rename)
    return df_players


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
  # Filtrar jogadores, onde: 
  # ID repete em temporada, é duplicada
  # Se for, pegar a linha onde time = TOV
  jogadores_temporada_duplicada = df.duplicated(subset=['JOGADOR_ID', 'TEMPORADA'], keep=False)
  df_temporada_unica = df[jogadores_temporada_duplicada & (df['TIME'] == 'TOT')]
  
  df_sem_duplicada = df.drop_duplicates(subset=['JOGADOR_ID', 'TEMPORADA'], keep=False)
  df_novo = pd.concat([df_temporada_unica, df_sem_duplicada], axis=0)
  return df_novo
           
        
def filtrar_volume_minimo(df: pd.DataFrame, jogos_minimo: int = 20) -> pd.DataFrame:
    filtro_jogos = df['JOGOS_JOGADOS'] >= jogos_minimo
    df_filtro_jogos = df[filtro_jogos]
    print(f"Jogadores abaixo dos 20 jogos minimos removidos {(len(df) - len(df_filtro_jogos))}")
    return df_filtro_jogos

def salvar_processado(df: pd.DataFrame):
    path = Path("../data/processed/nba_stats_clean.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    

def transformation_data():
    print(f'Iniciando transformação dos dados.')
    df = create_dataframe(path_name)
    df = rename_columns(df)
    df = remove_duplicates(df)
    df = filtrar_volume_minimo(df)
    salvar_processado(df)
    print(f'Transformação realizada. Dados tratados, com {len(df)} jogadores.')
    return df
   
transformation_data()
