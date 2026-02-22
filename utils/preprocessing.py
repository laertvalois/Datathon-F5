"""
Módulo de Pré-processamento Padronizado
Funções compartilhadas para pré-processamento de dados.
Mantém coerência entre análise exploratória e modelagem.
"""

import pandas as pd
import numpy as np
import re
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def standardize_numeric_columns(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Padroniza colunas numéricas: converte vírgula para ponto e para numérico.
    
    Args:
        df: DataFrame a ser processado
        columns: Lista de colunas a processar (None = todas numéricas)
        
    Returns:
        DataFrame com colunas padronizadas
    """
    df_clean = df.copy()
    
    if columns is None:
        # Identifica colunas que podem ser numéricas (exceto categóricas conhecidas)
        exclude_cols = ['RA', 'Turma', 'Fase', 'Instituição de ensino', 'Defasagem', 'Nivel_IAN']
        columns = [col for col in df_clean.columns if col not in exclude_cols]
    
    for col in columns:
        if col in df_clean.columns:
            # Converte para string, substitui vírgula por ponto
            df_clean[col] = df_clean[col].astype(str).str.replace(',', '.', regex=False)
            # Converte para numérico
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    return df_clean


def extract_fase_numeric(fase_value: Any) -> float:
    """
    Extrai valor numérico da fase, mantendo 'ALFA' como string especial.
    
    Args:
        fase_value: Valor da fase (pode ser string, número, etc.)
        
    Returns:
        Valor numérico da fase ou np.nan
    """
    if pd.isna(fase_value):
        return np.nan
    
    if isinstance(fase_value, str):
        if fase_value.upper() == 'ALFA':
            return 'ALFA'  # Mantém como string especial
        # Extrai números de sequências como '1A', 'FASE 1' ou '7'
        match = re.search(r'\d+', fase_value)
        if match:
            try:
                return float(match.group(0))
            except ValueError:
                return np.nan
        else:
            # Se for uma string numérica, converte
            try:
                return float(fase_value)
            except ValueError:
                return np.nan
    elif isinstance(fase_value, (int, float)):
        return float(fase_value)
    
    return np.nan


def standardize_fase_column(df: pd.DataFrame, column: str = 'Fase') -> pd.DataFrame:
    """
    Padroniza coluna de Fase.
    
    Args:
        df: DataFrame
        column: Nome da coluna de fase
        
    Returns:
        DataFrame com fase padronizada
    """
    df_clean = df.copy()
    
    if column in df_clean.columns:
        df_clean[column] = df_clean[column].apply(extract_fase_numeric)
    
    return df_clean


def fill_missing_with_median(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Preenche valores faltantes com mediana.
    
    Args:
        df: DataFrame
        columns: Lista de colunas (None = todas numéricas)
        
    Returns:
        DataFrame com valores faltantes preenchidos
    """
    df_clean = df.copy()
    
    if columns is None:
        columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in columns:
        if col in df_clean.columns:
            median_value = df_clean[col].median()
            if pd.notna(median_value):
                df_clean[col].fillna(median_value, inplace=True)
            else:
                logger.warning(f"Não foi possível calcular mediana para {col}")
    
    return df_clean


def calculate_inde_consolidated(df: pd.DataFrame) -> pd.Series:
    """
    Calcula INDE consolidado baseado no ano.
    
    Args:
        df: DataFrame com colunas Ano, INDE_22, INDE_23, INDE_24
        
    Returns:
        Series com INDE consolidado
    """
    conditions = [
        df['Ano'] == 2022,
        df['Ano'] == 2023,
        df['Ano'] == 2024
    ]
    
    choices = [
        df.get('INDE_22', pd.Series(index=df.index)),
        df.get('INDE_23', pd.Series(index=df.index)),
        df.get('INDE_24', pd.Series(index=df.index))
    ]
    
    return pd.Series(np.select(conditions, choices, default=np.nan), index=df.index)


def create_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features derivadas: Tempo_na_escola, Media_academica, Media_indicadores.
    
    Args:
        df: DataFrame com dados base
        
    Returns:
        DataFrame com features derivadas adicionadas
    """
    df_features = df.copy()
    
    # Tempo na escola
    if 'Ano' in df_features.columns and 'Ano ingresso' in df_features.columns:
        df_features['Tempo_na_escola'] = df_features['Ano'] - df_features['Ano ingresso']
    
    # Média acadêmica
    academic_cols = ['Mat', 'Por', 'Ing']
    if all(col in df_features.columns for col in academic_cols):
        df_features['Media_academica'] = df_features[academic_cols].mean(axis=1)
    
    # Média de indicadores
    indicator_cols = ['IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'IPV']
    if all(col in df_features.columns for col in indicator_cols):
        df_features['Media_indicadores'] = df_features[indicator_cols].mean(axis=1)
    
    return df_features


def create_target_variable(df: pd.DataFrame, column: str = 'IAN') -> pd.Series:
    """
    Cria variável target: Risco_defasagem.
    0 = sem risco (IAN == 10), 1 = em risco (IAN != 10)
    
    Args:
        df: DataFrame
        column: Nome da coluna IAN
        
    Returns:
        Series com target
    """
    if column not in df.columns:
        raise ValueError(f"Coluna {column} não encontrada no DataFrame")
    
    return df[column].apply(lambda x: 0 if x == 10 else 1)


def create_nivel_ian(df: pd.DataFrame, column: str = 'IAN') -> pd.Series:
    """
    Cria categorização de nível IAN.
    
    Args:
        df: DataFrame
        column: Nome da coluna IAN
        
    Returns:
        Series com categorias: 'severa', 'moderada', 'em fase'
    """
    if column not in df.columns:
        raise ValueError(f"Coluna {column} não encontrada no DataFrame")
    
    conditions = [
        df[column] < 5,
        (df[column] >= 5) & (df[column] <= 7)
    ]
    choices = ['severa', 'moderada']
    
    return pd.Series(
        np.select(conditions, choices, default='em fase'),
        index=df.index
    )


def preprocess_for_eda(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pré-processa dados para análise exploratória.
    Aplica todas as transformações necessárias de forma padronizada.
    
    Args:
        df: DataFrame bruto
        
    Returns:
        DataFrame pré-processado para EDA
    """
    logger.info("Iniciando pré-processamento para EDA...")
    
    # 1. Padroniza colunas numéricas
    numeric_cols = ['Idade', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'Mat', 'Por', 'Ing', 
                   'IPV', 'IAN', 'INDE_22', 'INDE_23', 'INDE_24', 'Ano ingresso']
    df = standardize_numeric_columns(df, columns=numeric_cols)
    
    # 2. Padroniza Fase
    df = standardize_fase_column(df)
    
    # 3. INDE já vem da base oficial (não recalcular)
    # Se não estiver presente, usa INDE consolidado do banco
    if 'INDE' not in df.columns or df['INDE'].isna().all():
        # Tenta consolidar do histórico (inde_22, inde_23, inde_24)
        if 'inde_22' in df.columns or 'inde_23' in df.columns or 'inde_24' in df.columns:
            df['INDE'] = calculate_inde_consolidated(df)
        # Se não tiver histórico, mantém NaN (será preenchido depois)
    
    # 4. Preenche valores faltantes
    fill_cols = ['IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'Mat', 'Por', 'Ing', 'IPV', 'IAN', 'INDE']
    df = fill_missing_with_median(df, columns=fill_cols)
    
    # 5. Cria features derivadas
    df = create_derived_features(df)
    
    # 6. Cria categorização de IAN
    df['Nivel_IAN'] = create_nivel_ian(df)
    
    logger.info("Pré-processamento para EDA concluído")
    return df


def preprocess_for_modeling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pré-processa dados para modelagem.
    Aplica todas as transformações necessárias de forma padronizada.
    
    Args:
        df: DataFrame bruto
        
    Returns:
        DataFrame pré-processado para modelagem
    """
    logger.info("Iniciando pré-processamento para modelagem...")
    
    # 1. Padroniza colunas numéricas
    numeric_cols = ['Idade', 'Ano ingresso', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
                   'Mat', 'Por', 'Ing', 'IPV', 'IAN']
    df = standardize_numeric_columns(df, columns=numeric_cols)
    
    # 2. Remove duplicatas
    initial_count = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_count:
        logger.info(f"Removidas {initial_count - len(df)} duplicatas")
    
    # 3. Cria features derivadas
    df = create_derived_features(df)
    
    # 4. Cria target
    df['Risco_defasagem'] = create_target_variable(df)
    
    logger.info("Pré-processamento para modelagem concluído")
    return df


def validate_data_ranges(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Valida ranges esperados dos dados.
    
    Args:
        df: DataFrame a validar
        
    Returns:
        Dicionário com warnings encontrados
    """
    warnings = {
        'out_of_range': [],
        'missing_values': []
    }
    
    # Ranges esperados (ajustar conforme necessário)
    ranges = {
        'IAN': (0, 10),
        'IDA': (0, 10),
        'IEG': (0, 10),
        'IAA': (0, 10),
        'IPS': (0, 10),
        'IPP': (0, 10),
        'IPV': (0, 10),
        'Mat': (0, 10),
        'Por': (0, 10),
        'Ing': (0, 10)
    }
    
    for col, (min_val, max_val) in ranges.items():
        if col in df.columns:
            # Verifica valores fora do range
            out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
            if len(out_of_range) > 0:
                warnings['out_of_range'].append(
                    f"{col}: {len(out_of_range)} valores fora do range [{min_val}, {max_val}]"
                )
            
            # Verifica valores faltantes
            missing = df[col].isna().sum()
            if missing > 0:
                warnings['missing_values'].append(
                    f"{col}: {missing} valores faltantes ({missing/len(df)*100:.1f}%)"
                )
    
    return warnings
