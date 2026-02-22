"""
Script de Migração: CSV → SQLite
Migra os dados dos CSVs do GitHub para o banco de dados SQLite local.
"""

import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path
from typing import Optional
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URLs dos CSVs originais
CSV_URLS = {
    2024: 'https://raw.githubusercontent.com/henriquebol/FIAP---DATATHON/refs/heads/main/data/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON%20-%20PEDE2024.csv',
    2023: 'https://raw.githubusercontent.com/henriquebol/FIAP---DATATHON/refs/heads/main/data/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON%20-%20PEDE2024.csv',
    2022: 'https://raw.githubusercontent.com/henriquebol/FIAP---DATATHON/refs/heads/main/data/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON%20-%20PEDE2022.csv'
}

# Mapeamento de colunas para padronização
COLUMN_MAPPING = {
    'Idade 22': 'Idade',
    'Matem': 'Mat',
    'Portug': 'Por',
    'Inglês': 'Ing',
    'INDE 22': 'INDE_22',
    'INDE 23': 'INDE_23',
    'INDE 2024': 'INDE_24'
}

# Mapeamento de colunas para o banco de dados
DB_COLUMN_MAPPING = {
    'RA': 'ra',
    'Ano': 'ano',
    'Turma': 'turma',
    'Idade': 'idade',
    'Ano ingresso': 'ano_ingresso',
    'Fase': 'fase',
    'Instituição de ensino': 'instituicao_ensino',
    'IAA': 'iaa',
    'IEG': 'ieg',
    'IPS': 'ips',
    'IPP': 'ipp',
    'IDA': 'ida',
    'IPV': 'ipv',
    'IAN': 'ian',
    'Mat': 'mat',
    'Por': 'por',
    'Ing': 'ing',
    'INDE_22': 'inde_22',
    'INDE_23': 'inde_23',
    'INDE_24': 'inde_24',
    'INDE': 'inde',
    'Defasagem': 'defasagem'
}


def get_db_path() -> Path:
    """Retorna o caminho do banco de dados."""
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / 'data' / 'datathon_f5.db'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def load_and_prepare_data(year: int) -> pd.DataFrame:
    """
    Carrega e prepara os dados de um ano específico.
    
    Args:
        year: Ano dos dados (2022, 2023 ou 2024)
        
    Returns:
        DataFrame preparado
    """
    logger.info(f"Carregando dados de {year}...")
    
    try:
        df = pd.read_csv(CSV_URLS[year])
    except Exception as e:
        logger.error(f"Erro ao carregar CSV de {year}: {e}")
        raise
    
    # Adiciona coluna de ano
    df['Ano'] = year
    
    # Renomeia colunas específicas de 2022
    if year == 2022:
        df.rename(columns=COLUMN_MAPPING, inplace=True)
    
    # Renomeia colunas de INDE
    df.rename(columns={
        'INDE 22': 'INDE_22',
        'INDE 23': 'INDE_23',
        'INDE 2024': 'INDE_24'
    }, inplace=True, errors='ignore')
    
    logger.info(f"Dados de {year} carregados: {len(df)} registros")
    return df


def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza os dados: conversões numéricas, tratamento de valores faltantes.
    
    Args:
        df: DataFrame a ser padronizado
        
    Returns:
        DataFrame padronizado
    """
    logger.info("Padronizando dados...")
    
    # Cria cópia para não modificar o original
    df_clean = df.copy()
    
    # Converte vírgula para ponto em colunas numéricas
    numeric_cols = df_clean.select_dtypes(include=['object']).columns
    for col in numeric_cols:
        if col not in ['RA', 'Turma', 'Fase', 'Instituição de ensino', 'Defasagem']:
            df_clean[col] = df_clean[col].astype(str).str.replace(',', '.', regex=False)
    
    # Converte para numérico
    numeric_columns = ['Idade', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'Mat', 'Por', 'Ing', 
                      'IPV', 'IAN', 'INDE_22', 'INDE_23', 'INDE_24', 'INDE', 'Ano ingresso']
    
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Remove duplicatas
    initial_count = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    duplicates_removed = initial_count - len(df_clean)
    if duplicates_removed > 0:
        logger.info(f"Removidas {duplicates_removed} duplicatas")
    
    # Calcula INDE consolidado baseado no ano
    if 'INDE' not in df_clean.columns or df_clean['INDE'].isna().all():
        # Garante que todas as colunas existam, preenchendo com NaN se não existirem
        for col in ['INDE_22', 'INDE_23', 'INDE_24']:
            if col not in df_clean.columns:
                df_clean[col] = np.nan
        
        conditions = [
            df_clean['Ano'] == 2022,
            df_clean['Ano'] == 2023,
            df_clean['Ano'] == 2024
        ]
        choices = [
            df_clean['INDE_22'],
            df_clean['INDE_23'],
            df_clean['INDE_24']
        ]
        df_clean['INDE'] = pd.Series(np.select(conditions, choices, default=np.nan), index=df_clean.index)
    
    logger.info("Dados padronizados com sucesso")
    return df_clean


def map_to_db_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mapeia colunas do DataFrame para nomes do banco de dados.
    
    Args:
        df: DataFrame com colunas originais
        
    Returns:
        DataFrame com colunas mapeadas
    """
    df_mapped = df.copy()
    
    # Renomeia colunas para nomes do banco
    rename_dict = {k: v for k, v in DB_COLUMN_MAPPING.items() if k in df_mapped.columns}
    df_mapped.rename(columns=rename_dict, inplace=True)
    
    return df_mapped


def insert_data_to_db(df: pd.DataFrame, conn: sqlite3.Connection, replace: bool = False):
    """
    Insere dados no banco de dados.
    
    Args:
        df: DataFrame com dados a serem inseridos
        conn: Conexão com o banco de dados
        replace: Se True, substitui dados existentes
    """
    logger.info(f"Inserindo {len(df)} registros no banco de dados...")
    
    # Seleciona apenas colunas que existem na tabela
    table_columns = [
        'ra', 'ano', 'turma', 'idade', 'ano_ingresso', 'fase', 'instituicao_ensino',
        'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian',
        'mat', 'por', 'ing',
        'inde_22', 'inde_23', 'inde_24', 'inde', 'defasagem'
    ]
    
    # Filtra apenas colunas que existem no DataFrame e na tabela
    available_columns = [col for col in table_columns if col in df.columns]
    df_to_insert = df[available_columns].copy()
    
    # Preenche valores faltantes com None para o SQLite
    df_to_insert = df_to_insert.where(pd.notnull(df_to_insert), None)
    
    # Prepara query
    columns_str = ', '.join(available_columns)
    placeholders = ', '.join(['?' for _ in available_columns])
    
    if replace:
        query = f"""
        INSERT OR REPLACE INTO alunos ({columns_str})
        VALUES ({placeholders})
        """
    else:
        query = f"""
        INSERT INTO alunos ({columns_str})
        VALUES ({placeholders})
        """
    
    # Insere dados
    cursor = conn.cursor()
    try:
        cursor.executemany(query, df_to_insert.values.tolist())
        conn.commit()
        logger.info(f"✓ {len(df_to_insert)} registros inseridos com sucesso")
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao inserir dados: {e}")
        raise


def calculate_derived_features(conn: sqlite3.Connection):
    """
    Calcula e insere features derivadas na tabela features_derivadas.
    
    Args:
        conn: Conexão com o banco de dados
    """
    logger.info("Calculando features derivadas...")
    
    cursor = conn.cursor()
    
    # Limpa features antigas
    cursor.execute("DELETE FROM features_derivadas")
    
    # Calcula e insere features derivadas
    query = """
    INSERT INTO features_derivadas (
        aluno_id,
        tempo_na_escola,
        media_academica,
        media_indicadores,
        risco_defasagem,
        nivel_ian
    )
    SELECT 
        id,
        ano - ano_ingresso as tempo_na_escola,
        (mat + por + ing) / 3.0 as media_academica,
        (iaa + ieg + ips + ipp + ida + ipv) / 6.0 as media_indicadores,
        CASE WHEN ian = 10 THEN 0 ELSE 1 END as risco_defasagem,
        CASE 
            WHEN ian < 5 THEN 'severa'
            WHEN ian >= 5 AND ian <= 7 THEN 'moderada'
            ELSE 'em fase'
        END as nivel_ian
    FROM alunos
    WHERE ano_ingresso IS NOT NULL
    """
    
    try:
        cursor.execute(query)
        conn.commit()
        count = cursor.rowcount
        logger.info(f"✓ {count} features derivadas calculadas e inseridas")
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao calcular features derivadas: {e}")
        raise


def migrate_all_data(force: bool = False):
    """
    Migra todos os dados dos CSVs para o banco de dados SQLite.
    
    Args:
        force: Se True, substitui dados existentes
    """
    db_path = get_db_path()
    
    logger.info("=" * 60)
    logger.info("INICIANDO MIGRAÇÃO CSV → SQLite")
    logger.info("=" * 60)
    logger.info(f"Banco de dados: {db_path}")
    
    # Cria conexão com o banco
    conn = sqlite3.connect(str(db_path))
    
    try:
        # Carrega schema se não existir
        schema_path = Path(__file__).parent / 'schema.sql'
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            logger.info("✓ Schema do banco criado/verificado")
        
        # Carrega e migra dados de cada ano
        all_data = []
        for year in [2022, 2023, 2024]:
            df = load_and_prepare_data(year)
            df_clean = standardize_data(df)
            all_data.append(df_clean)
        
        # Concatena todos os anos
        df_combined = pd.concat(all_data, ignore_index=True)
        logger.info(f"Total de registros combinados: {len(df_combined)}")
        
        # Mapeia para colunas do banco
        df_mapped = map_to_db_columns(df_combined)
        
        # Insere no banco
        if force:
            logger.warning("Modo FORCE ativado - dados existentes serão substituídos")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alunos")
            conn.commit()
        
        insert_data_to_db(df_mapped, conn, replace=force)
        
        # Calcula features derivadas
        calculate_derived_features(conn)
        
        # Estatísticas finais
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alunos")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alunos WHERE ano = 2022")
        count_2022 = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alunos WHERE ano = 2023")
        count_2023 = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alunos WHERE ano = 2024")
        count_2024 = cursor.fetchone()[0]
        
        logger.info("=" * 60)
        logger.info("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("=" * 60)
        logger.info(f"Total de registros: {total}")
        logger.info(f"  - 2022: {count_2022}")
        logger.info(f"  - 2023: {count_2023}")
        logger.info(f"  - 2024: {count_2024}")
        logger.info(f"Banco de dados: {db_path}")
        
    except Exception as e:
        logger.error(f"Erro durante migração: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    import sys
    import numpy as np
    
    force = '--force' in sys.argv
    
    try:
        migrate_all_data(force=force)
    except Exception as e:
        logger.error(f"Migração falhou: {e}")
        sys.exit(1)
