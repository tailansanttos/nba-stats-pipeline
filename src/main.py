from ingestion import extract_data_players
from pathlib import Path
from transformation import transformation_data
from aggregation import aggregation_data
from nba_api.stats.endpoints import leagueleaders
import pandas as pd

TEMPORADAS = ["2024-25", "2023-24", "2022-23", "2021-22", "2020-21"]
path_name_aggregation = Path(__file__).parent.parent / 'data' / 'processed' / 'nba_stats_clean.csv'


def pipeline_dados():
    try: 
        print(f'Iniciando processo de ETL. ')
        print(f'1. Extração dos dados da API da NBA. ')
        df = extract_data_players()

        print(f'2. Transformação dos dados')
        df = transformation_data()

        print(f'2. Aggregação dos dados')
        aggregation_data()

    except Exception as e:
        print(f'Erro na pipeline de dados: {e}')
pipeline_dados()
    