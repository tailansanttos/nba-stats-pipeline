import pandas as pd
from pathlib import Path

path_name = Path(__file__).parent.parent / 'data' / 'processed' / 'nba_stats_clean.csv'
def carregar_dados_processados(path_name: str) -> pd.DataFrame:

    print(f'Iniciando carregamento dos dados processados.')
    path = Path(path_name)

    if not path.exists():
        print(f'Arquivo não encontrado. Tente novamente')
        return pd.DataFrame()

    df = pd.read_csv(path)
    print(f'Arquivo encontrado. Contém {len(df)} linhas.')
    return df

def top_pontuadores_por_temporada(df:pd.DataFrame) -> pd.DataFrame:
    df_pontuadores = df.sort_values(by='PTS', ascending=False).groupby('TEMPORADA').head(10)
    return df_pontuadores


def media_por_time(df: pd.DataFrame) -> pd.DataFrame:
    df_agrupado_time = df.groupby(by=['TIME', 'TEMPORADA']).agg({'PTS': 'mean'}).sort_values(by='PTS', ascending= False)
    return df_agrupado_time


def lider_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    categorias = ['REB', 'AST', 'STL', 'BLK']
    dfs = []
    for categoria in categorias:
        idx_categoria = df.groupby('TEMPORADA')[categoria].idxmax()
        df_cat = df.loc[idx_categoria][['TEMPORADA', 'JOGADOR']].copy()
        df_cat['CATEGORIA'] = categoria
        dfs.append(df_cat)
    df_lideres = pd.concat(dfs, ignore_index=True)
    return df_lideres

def evolucao_jogador(df:pd.DataFrame, jogador:str) -> pd.DataFrame:
    filtro_jogador = df['JOGADOR'] == jogador
    df_jogador = df[filtro_jogador]
    df_jogador = df_jogador[['TEMPORADA', 'JOGADOR', 'PTS']]
    return df_jogador

def salvar_agregados(df_pontuadores, df_media_time, df_lider_categoria, df_evolucao_jogador):
    path_lider_categoria = Path("../data/processed/nba_lider_por_categoria.csv")
    path_evolucao_jogador = Path("../data/processed/nba_evolucao_jogador.csv")
    path_pontuadores = Path("../data/processed/nba_pontuadores_por_temporada.csv")
    path_media_time = Path("../data/processed/nba_media_time.csv")

    exists_path(path_pontuadores, df_pontuadores)
    exists_path(path_media_time, df_media_time)
    exists_path(path_evolucao_jogador, df_evolucao_jogador)
    exists_path(path_lider_categoria, df_lider_categoria)



def exists_path(path: Path, df: pd.DataFrame):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)

def aggregation_data():
    print(f'Iniciando aggregação dos dados')
    jogador = input("Digite o nome do jogador: ")
    df = carregar_dados_processados(path_name)
    df_pontuadores = top_pontuadores_por_temporada(df)
    df_media_time = media_por_time(df)
    df_lider_categoria = lider_por_categoria(df)
    df_evolucao_jogador = evolucao_jogador(df, jogador)
    salvar_agregados(df_pontuadores, df_media_time, df_lider_categoria, df_evolucao_jogador)
    print(f'Dados agregados com sucesso.')

aggregation_data()