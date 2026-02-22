"""
Funções para cálculos conforme definições PEDE 2020.
"""

import pandas as pd
import numpy as np
import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def calcular_inde_pede(
    df: pd.DataFrame,
    fase_col: str = 'Fase',
    validar: bool = True
) -> pd.DataFrame:
    """
    Calcula INDE conforme ponderações oficiais do PEDE 2020.
    
    Args:
        df: DataFrame com os indicadores
        fase_col: Nome da coluna de fase
        validar: Se True, valida se todos os indicadores necessários estão presentes
        
    Returns:
        DataFrame com coluna 'INDE_calculado' adicionada
    """
    df = df.copy()
    
    # Indicadores necessários
    indicadores_fases_0_7 = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPP', 'IPV']
    indicadores_fase_8 = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS']
    
    if validar:
        # Valida indicadores para Fases 0-7
        missing_0_7 = [ind for ind in indicadores_fases_0_7 if ind not in df.columns]
        if missing_0_7:
            logger.warning(f"Indicadores faltantes para Fases 0-7: {missing_0_7}")
        
        # Valida indicadores para Fase 8
        missing_8 = [ind for ind in indicadores_fase_8 if ind not in df.columns]
        if missing_8:
            logger.warning(f"Indicadores faltantes para Fase 8: {missing_8}")
    
    # Inicializa coluna
    df['INDE_calculado'] = np.nan
    
    # Normaliza valores de Fase
    def normalize_fase(fase_value):
        """Normaliza valor de fase para comparação."""
        if pd.isna(fase_value):
            return np.nan
        if isinstance(fase_value, str):
            fase_upper = fase_value.upper()
            if fase_upper == 'ALFA':
                return 0  # ALFA equivale a Fase 0
            # Extrai número do início da string (ex: '1A' -> 1, '2B' -> 2)
            match = re.match(r'^(\d+)', fase_value)
            if match:
                try:
                    return float(match.group(1))
                except:
                    return np.nan
            try:
                return float(fase_value)
            except:
                return np.nan
        return float(fase_value)
    
    df['_fase_normalizada'] = df[fase_col].apply(normalize_fase)
    
    # Fases 0 a 7 (incluindo ALFA = 0 e variações como 1A, 2B, etc.)
    mask_fases_0_7 = (
        (df['_fase_normalizada'] >= 0) & 
        (df['_fase_normalizada'] <= 7)
    ) | (df[fase_col].astype(str).str.upper() == 'ALFA')
    
    if mask_fases_0_7.any():
        df.loc[mask_fases_0_7, 'INDE_calculado'] = (
            df.loc[mask_fases_0_7, 'IAN'] * 0.1 +
            df.loc[mask_fases_0_7, 'IDA'] * 0.2 +
            df.loc[mask_fases_0_7, 'IEG'] * 0.2 +
            df.loc[mask_fases_0_7, 'IAA'] * 0.1 +
            df.loc[mask_fases_0_7, 'IPS'] * 0.1 +
            df.loc[mask_fases_0_7, 'IPP'] * 0.1 +
            df.loc[mask_fases_0_7, 'IPV'] * 0.2
        )
    
    # Fase 8
    mask_fase_8 = df['_fase_normalizada'] == 8
    
    if mask_fase_8.any():
        df.loc[mask_fase_8, 'INDE_calculado'] = (
            df.loc[mask_fase_8, 'IAN'] * 0.1 +
            df.loc[mask_fase_8, 'IDA'] * 0.4 +
            df.loc[mask_fase_8, 'IEG'] * 0.2 +
            df.loc[mask_fase_8, 'IAA'] * 0.1 +
            df.loc[mask_fase_8, 'IPS'] * 0.2
        )
    
    # Remove coluna auxiliar
    df.drop('_fase_normalizada', axis=1, inplace=True)
    
    logger.info(f"INDE calculado para {df['INDE_calculado'].notna().sum()} registros")
    
    return df


def validar_inde_calculado(
    df: pd.DataFrame,
    inde_original_col: str = 'INDE',
    inde_calculado_col: str = 'INDE_calculado',
    tolerancia: float = 0.01
) -> pd.DataFrame:
    """
    Valida se o INDE calculado está próximo do INDE original.
    
    Args:
        df: DataFrame com INDE original e calculado
        inde_original_col: Nome da coluna com INDE original
        inde_calculado_col: Nome da coluna com INDE calculado
        tolerancia: Tolerância para diferença (padrão: 0.01)
        
    Returns:
        DataFrame com coluna 'INDE_diferenca' e 'INDE_valido'
    """
    df = df.copy()
    
    if inde_original_col not in df.columns:
        logger.warning(f"Coluna {inde_original_col} não encontrada")
        return df
    
    if inde_calculado_col not in df.columns:
        logger.warning(f"Coluna {inde_calculado_col} não encontrada. Execute calcular_inde_pede primeiro.")
        return df
    
    # Calcula diferença
    mask_both = df[inde_original_col].notna() & df[inde_calculado_col].notna()
    df['INDE_diferenca'] = np.nan
    df.loc[mask_both, 'INDE_diferenca'] = abs(
        df.loc[mask_both, inde_original_col] - 
        df.loc[mask_both, inde_calculado_col]
    )
    
    # Valida (dentro da tolerância)
    df['INDE_valido'] = df['INDE_diferenca'] <= tolerancia
    
    # Estatísticas
    total_comparavel = mask_both.sum()
    if total_comparavel > 0:
        validos = df['INDE_valido'].sum()
        logger.info(f"INDE validado: {validos}/{total_comparavel} ({validos/total_comparavel*100:.1f}%)")
        
        if validos < total_comparavel:
            diferenca_media = df.loc[mask_both, 'INDE_diferenca'].mean()
            diferenca_max = df.loc[mask_both, 'INDE_diferenca'].max()
            logger.warning(f"Diferença média: {diferenca_media:.4f}, máxima: {diferenca_max:.4f}")
    
    return df


def criar_target_risco_ian(
    df: pd.DataFrame,
    ian_col: str = 'IAN',
    metodo: str = 'binario_10'
) -> pd.Series:
    """
    Cria variável target de risco baseada no IAN.
    
    Args:
        df: DataFrame
        ian_col: Nome da coluna IAN
        metodo: Método de criação do target
            - 'binario_10': Risco = 0 se IAN == 10, senão 1 (atual)
            - 'binario_7': Risco = 0 se IAN >= 7, senão 1
            - 'multiclasse': 0=sem risco (IAN==10), 1=moderado (5<=IAN<10), 2=severa (IAN<5)
        
    Returns:
        Series com target
    """
    if ian_col not in df.columns:
        raise ValueError(f"Coluna {ian_col} não encontrada")
    
    if metodo == 'binario_10':
        # Método atual: IAN == 10 = sem risco
        return df[ian_col].apply(lambda x: 0 if x == 10 else 1)
    
    elif metodo == 'binario_7':
        # Alternativa: IAN >= 7 = sem risco
        return df[ian_col].apply(lambda x: 0 if x >= 7 else 1)
    
    elif metodo == 'multiclasse':
        # Multiclasse: 0=sem risco, 1=moderado, 2=severa
        conditions = [
            df[ian_col] == 10,
            (df[ian_col] >= 5) & (df[ian_col] < 10)
        ]
        choices = [0, 1]  # 0=sem risco, 1=moderado
        return pd.Series(
            np.select(conditions, choices, default=2),  # 2=severa
            index=df.index
        )
    else:
        raise ValueError(f"Método '{metodo}' não reconhecido")


def documentar_ponderacoes_inde() -> dict:
    """
    Retorna dicionário com ponderações oficiais do INDE conforme PEDE 2020.
    
    Returns:
        Dicionário com ponderações por fase
    """
    return {
        'fases_0_7': {
            'IAN': 0.1,
            'IDA': 0.2,
            'IEG': 0.2,
            'IAA': 0.1,
            'IPS': 0.1,
            'IPP': 0.1,
            'IPV': 0.2,
            'total': 1.0
        },
        'fase_8': {
            'IAN': 0.1,
            'IDA': 0.4,
            'IEG': 0.2,
            'IAA': 0.1,
            'IPS': 0.2,
            'total': 1.0
        }
    }
