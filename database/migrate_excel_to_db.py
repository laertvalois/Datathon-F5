"""
Script de Migração: Excel Oficial → SQLite
Migra os dados da base oficial Excel para o banco de dados SQLite local.
Usa INDE já calculado na base oficial.
"""

import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
from typing import Optional
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_db_path() -> Path:
    """Retorna o caminho do banco de dados."""
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / 'data' / 'datathon_f5.db'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_excel_path() -> Path:
    """Retorna o caminho do Excel oficial."""
    base_dir = Path(__file__).parent.parent
    excel_path = base_dir / 'Colab' / 'Datathon' / 'BASE DE DADOS PEDE 2024 - DATATHON.xlsx'
    return excel_path


def load_excel_sheet(sheet_name: str, year: int) -> pd.DataFrame:
    """
    Carrega uma planilha específica do Excel oficial.
    
    Args:
        sheet_name: Nome da planilha (PEDE2022, PEDE2023, PEDE2024)
        year: Ano correspondente
        
    Returns:
        DataFrame com dados da planilha
    """
    excel_path = get_excel_path()
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Arquivo Excel não encontrado: {excel_path}")
    
    logger.info(f"Carregando planilha {sheet_name} (ano {year})...")
    
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df['Ano'] = year
        logger.info(f"Planilha {sheet_name} carregada: {len(df)} registros, {len(df.columns)} colunas")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar planilha {sheet_name}: {e}")
        raise


def standardize_columns(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Padroniza colunas entre diferentes anos.
    
    Args:
        df: DataFrame a padronizar
        year: Ano dos dados
        
    Returns:
        DataFrame com colunas padronizadas
    """
    df_clean = df.copy()
    
    # Mapeamento de colunas por ano
    column_mapping = {
        2022: {
            'Idade 22': 'Idade',
            'Matem': 'Mat',
            'Portug': 'Por',
            'Inglês': 'Ing',
            'INDE 22': 'INDE',
            'Ano nasc': 'Ano_nasc',
            'Gênero': 'Genero',
            'Instituição de ensino': 'Instituicao_ensino',
            'Pedra 20': 'Pedra_20',
            'Pedra 21': 'Pedra_21',
            'Pedra 22': 'Pedra_22',
            'Fase ideal': 'Fase_ideal',
            'Defas': 'Defasagem',
            'Destaque IEG': 'Destaque_IEG',
            'Destaque IDA': 'Destaque_IDA',
            'Destaque IPV': 'Destaque_IPV'
        },
        2023: {
            'INDE 2023': 'INDE',
            'INDE 23': 'INDE_23',
            'Pedra 2023': 'Pedra_23',
            'Nome Anonimizado': 'Nome',
            'Data de Nasc': 'Data_nasc',
            'Gênero': 'Genero',
            'Instituição de ensino': 'Instituicao_ensino',
            'Pedra 20': 'Pedra_20',
            'Pedra 21': 'Pedra_21',
            'Pedra 22': 'Pedra_22',
            'Pedra 23': 'Pedra_23',
            'Fase Ideal': 'Fase_ideal',
            'Destaque IEG': 'Destaque_IEG',
            'Destaque IDA': 'Destaque_IDA',
            'Destaque IPV': 'Destaque_IPV',
            'Destaque IPV.1': 'Destaque_IPV_2'
        },
        2024: {
            'INDE 2024': 'INDE',
            'Pedra 2024': 'Pedra_24',
            'Nome Anonimizado': 'Nome',
            'Data de Nasc': 'Data_nasc',
            'Gênero': 'Genero',
            'Instituição de ensino': 'Instituicao_ensino',
            'Pedra 20': 'Pedra_20',
            'Pedra 21': 'Pedra_21',
            'Pedra 22': 'Pedra_22',
            'Pedra 23': 'Pedra_23',
            'Pedra 24': 'Pedra_24',
            'Fase Ideal': 'Fase_ideal',
            'Destaque IEG': 'Destaque_IEG',
            'Destaque IDA': 'Destaque_IDA',
            'Destaque IPV': 'Destaque_IPV',
            'Ativo/ Inativo': 'Status',
            'Ativo/ Inativo.1': 'Status_2'
        }
    }
    
    # Aplica mapeamento
    if year in column_mapping:
        df_clean.rename(columns=column_mapping[year], inplace=True)
    
    # Padroniza nomes de colunas (remove espaços, acentos, etc.)
    df_clean.columns = df_clean.columns.str.strip()
    
    # Garante que colunas de INDE histórico estão presentes
    if year == 2022:
        if 'INDE_22' not in df_clean.columns and 'INDE' in df_clean.columns:
            df_clean['INDE_22'] = df_clean['INDE']
    elif year == 2023:
        if 'INDE_23' not in df_clean.columns and 'INDE' in df_clean.columns:
            df_clean['INDE_23'] = df_clean['INDE']
    elif year == 2024:
        if 'INDE_24' not in df_clean.columns and 'INDE' in df_clean.columns:
            df_clean['INDE_24'] = df_clean['INDE']
    
    return df_clean


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas numéricas, tratando vírgulas e valores inválidos.
    
    Args:
        df: DataFrame a converter
        
    Returns:
        DataFrame com colunas numéricas convertidas
    """
    df_clean = df.copy()
    
    # Colunas numéricas esperadas
    numeric_cols = [
        'Idade', 'Ano_ingresso', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 
        'IPV', 'IAN', 'Mat', 'Por', 'Ing', 'INDE', 'INDE_22', 'INDE_23', 'INDE_24'
    ]
    
    for col in numeric_cols:
        if col in df_clean.columns:
            # Converte para string primeiro para tratar vírgulas
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].astype(str).str.replace(',', '.', regex=False)
            
            # Converte para numérico
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    return df_clean


def map_to_db_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mapeia colunas do DataFrame para colunas do banco de dados.
    
    Args:
        df: DataFrame com colunas padronizadas
        
    Returns:
        DataFrame mapeado para estrutura do banco
    """
    df_mapped = pd.DataFrame()
    
    # Mapeamento direto (prioridade: mais específico primeiro)
    mapping = {
        'RA': 'ra',
        'Ano': 'ano',
        'Turma': 'turma',
        'Idade': 'idade',
        'Ano_ingresso': 'ano_ingresso',
        'Ano ingresso': 'ano_ingresso',
        'Fase': 'fase',
        'Instituicao_ensino': 'instituicao_ensino',
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
        'Defasagem': 'defasagem',
        'Defas': 'defasagem',
        'Pedra_20': 'pedra_20',
        'Pedra_21': 'pedra_21',
        'Pedra_22': 'pedra_22',
        'Pedra_23': 'pedra_23',
        'Pedra_24': 'pedra_24',
        'Fase_ideal': 'fase_ideal',
        'Destaque_IEG': 'destaque_ieg',
        'Destaque_IDA': 'destaque_ida',
        'Destaque_IPV': 'destaque_ipv'
    }
    
    # Remove duplicatas de colunas antes de mapear
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Aplica mapeamento (evita duplicatas)
    used_targets = set()
    for source_col, target_col in mapping.items():
        if source_col in df.columns and target_col not in used_targets:
            df_mapped[target_col] = df[source_col]
            used_targets.add(target_col)
    
    # Garante que ano está presente
    if 'ano' not in df_mapped.columns and 'Ano' in df.columns:
        df_mapped['ano'] = df['Ano']
    
    return df_mapped


def consolidate_inde(df: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida INDE dos diferentes anos.
    
    Args:
        df: DataFrame com colunas inde_22, inde_23, inde_24
        
    Returns:
        DataFrame com coluna inde consolidada
    """
    df_clean = df.copy()
    
    # Inicializa coluna inde
    df_clean['inde'] = np.nan
    
    # Consolida INDE baseado no ano
    mask_2022 = df_clean['ano'] == 2022
    mask_2023 = df_clean['ano'] == 2023
    mask_2024 = df_clean['ano'] == 2024
    
    if 'inde_22' in df_clean.columns:
        df_clean.loc[mask_2022, 'inde'] = df_clean.loc[mask_2022, 'inde_22']
    
    if 'inde_23' in df_clean.columns:
        df_clean.loc[mask_2023, 'inde'] = df_clean.loc[mask_2023, 'inde_23']
    
    if 'inde_24' in df_clean.columns:
        df_clean.loc[mask_2024, 'inde'] = df_clean.loc[mask_2024, 'inde_24']
    
    return df_clean


def insert_data_to_db(df: pd.DataFrame, conn: sqlite3.Connection, replace: bool = False):
    """
    Insere dados no banco de dados.
    
    Args:
        df: DataFrame com dados mapeados
        conn: Conexão com o banco
        replace: Se True, substitui dados existentes
    """
    logger.info(f"Inserindo {len(df)} registros no banco...")
    
    cursor = conn.cursor()
    
    if replace:
        cursor.execute("DELETE FROM alunos")
        conn.commit()
        logger.info("Dados antigos removidos")
    
    # Colunas do banco
    db_columns = [
        'ra', 'ano', 'turma', 'idade', 'ano_ingresso', 'fase',
        'instituicao_ensino', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian',
        'mat', 'por', 'ing', 'inde_22', 'inde_23', 'inde_24', 'inde',
        'defasagem', 'pedra_20', 'pedra_21', 'pedra_22', 'pedra_23', 'pedra_24',
        'fase_ideal', 'destaque_ieg', 'destaque_ida', 'destaque_ipv'
    ]
    
    # Prepara dados para inserção
    records = []
    for _, row in df.iterrows():
        record = []
        for col in db_columns:
            value = row.get(col, None)
            # Converte NaN para None
            if pd.isna(value):
                value = None
            record.append(value)
        records.append(record)
    
    # Insere em lote
    placeholders = ','.join(['?' for _ in db_columns])
    query = f"""
    INSERT INTO alunos ({','.join(db_columns)})
    VALUES ({placeholders})
    """
    
    try:
        cursor.executemany(query, records)
        conn.commit()
        logger.info(f"[OK] {len(records)} registros inseridos com sucesso")
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
        logger.info(f"[OK] {count} features derivadas calculadas e inseridas")
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao calcular features derivadas: {e}")
        raise


def migrate_all_data(force: bool = False):
    """
    Migra todos os dados do Excel oficial para o banco de dados SQLite.
    
    Args:
        force: Se True, substitui dados existentes
    """
    db_path = get_db_path()
    excel_path = get_excel_path()
    
    logger.info("=" * 60)
    logger.info("INICIANDO MIGRACAO EXCEL OFICIAL -> SQLite")
    logger.info("=" * 60)
    logger.info(f"Excel: {excel_path}")
    logger.info(f"Banco: {db_path}")
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Arquivo Excel não encontrado: {excel_path}")
    
    # Cria conexão com o banco
    conn = sqlite3.connect(str(db_path))
    
    try:
        # Carrega schema se não existir
        schema_path = Path(__file__).parent / 'schema.sql'
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            logger.info("[OK] Schema do banco criado/verificado")
        
        # Carrega e migra dados de cada ano
        all_data = []
        sheet_mapping = {
            'PEDE2022': 2022,
            'PEDE2023': 2023,
            'PEDE2024': 2024
        }
        
        for sheet_name, year in sheet_mapping.items():
            df = load_excel_sheet(sheet_name, year)
            df_clean = standardize_columns(df, year)
            # Remove colunas duplicadas
            df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()]
            df_numeric = convert_numeric_columns(df_clean)
            all_data.append(df_numeric)
        
        # Concatena todos os anos (reseta índices para evitar problemas)
        for i, df in enumerate(all_data):
            all_data[i] = df.reset_index(drop=True)
        
        try:
            df_combined = pd.concat(all_data, ignore_index=True, sort=False)
            logger.info(f"Total de registros combinados: {len(df_combined)}")
        except Exception as e:
            logger.error(f"Erro ao concatenar DataFrames: {e}")
            # Verifica colunas duplicadas
            for i, df in enumerate(all_data):
                dup_cols = df.columns[df.columns.duplicated()].tolist()
                if dup_cols:
                    logger.error(f"DataFrame {i} tem colunas duplicadas: {dup_cols}")
            raise
        
        # Mapeia para colunas do banco
        try:
            df_mapped = map_to_db_columns(df_combined)
            logger.info(f"Colunas mapeadas: {len(df_mapped.columns)}")
        except Exception as e:
            logger.error(f"Erro ao mapear colunas: {e}")
            logger.error(f"Colunas do DataFrame combinado: {df_combined.columns.tolist()}")
            raise
        
        # Consolida INDE
        try:
            df_mapped = consolidate_inde(df_mapped)
        except Exception as e:
            logger.error(f"Erro ao consolidar INDE: {e}")
            raise
        
        # Insere no banco
        if force:
            logger.warning("Modo FORCE ativado - dados existentes serao substituidos")
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
        logger.info("MIGRACAO CONCLUIDA COM SUCESSO!")
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
    
    force = '--force' in sys.argv
    
    try:
        migrate_all_data(force=force)
    except Exception as e:
        logger.error(f"Migração falhou: {e}")
        sys.exit(1)
