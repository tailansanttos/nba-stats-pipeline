import pandas as pd
from pathlib import Path
from nba_api.stats.endpoints import leagueleaders
import time

TEMPORADAS = ["2024-25", "2023-24", "2022-23", "2021-22", "2020-21"]


# 1. Extrair os dados da API, pegar os jogadores.
def extract_data_players() -> pd.DataFrame:
    all_stats = []
 
    for temporada in TEMPORADAS:
        print(f'Buscando dados da temporada {temporada}')

        dados = leagueleaders.LeagueLeaders(season=temporada)
        df_jogadores = dados.get_data_frames()[0]
        df_jogadores["temporada"] = temporada
        all_stats.append(df_jogadores)
        time.sleep(2)
    
    df_final = pd.concat(all_stats, ignore_index=True)

    output_path = Path('../data/raw/nba_players.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(output_path, index=False)


    print(f'Arquivo salvo em {output_path}')
    return df_final
extract_data_players()