"""
Módulo de Acesso ao Banco de Dados
Abstração para acesso aos dados do Datathon F5 via SQLite.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gerenciador de acesso ao banco de dados SQLite."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco. Se None, usa o padrão.
        """
        if db_path is None:
            base_dir = Path(__file__).parent.parent
            db_path = base_dir / 'data' / 'datathon_f5.db'
        
        self.db_path = Path(db_path)
        
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Banco de dados não encontrado: {self.db_path}\n"
                f"Execute o script de migração: python database/migrate_csv_to_db.py"
            )
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco de dados."""
        return sqlite3.connect(str(self.db_path))
    
    def load_data(
        self,
        years: Optional[List[int]] = None,
        columns: Optional[List[str]] = None,
        include_features: bool = True
    ) -> pd.DataFrame:
        """
        Carrega dados dos alunos do banco de dados.
        
        Args:
            years: Lista de anos para filtrar (None = todos)
            columns: Lista de colunas específicas (None = todas)
            include_features: Se True, inclui features derivadas
            
        Returns:
            DataFrame com os dados
        """
        conn = self.get_connection()
        
        try:
            if include_features:
                query = "SELECT * FROM vw_alunos_completo WHERE 1=1"
            else:
                query = "SELECT * FROM alunos WHERE 1=1"
            
            params = []
            
            if years:
                placeholders = ','.join(['?' for _ in years])
                query += f" AND ano IN ({placeholders})"
                params.extend(years)
            
            df = pd.read_sql_query(query, conn, params=params)
            
            if columns:
                # Mapeia nomes de colunas do código para nomes do banco
                available_cols = [col for col in columns if col in df.columns]
                if not available_cols:
                    # Tenta mapear de volta
                    reverse_mapping = {
                        'Ano': 'ano',
                        'RA': 'ra',
                        'Turma': 'turma',
                        'Idade': 'idade',
                        'Ano ingresso': 'ano_ingresso',
                        'Fase': 'fase',
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
                        'INDE': 'inde',
                        'Defasagem': 'defasagem'
                    }
                    available_cols = [
                        reverse_mapping.get(col, col) 
                        for col in columns 
                        if reverse_mapping.get(col, col) in df.columns
                    ]
                df = df[available_cols]
            
            return df
            
        finally:
            conn.close()
    
    def load_data_for_eda(self) -> pd.DataFrame:
        """
        Carrega dados formatados para análise exploratória.
        Retorna DataFrame com nomes de colunas padronizados.
        
        Returns:
            DataFrame formatado para EDA
        """
        df = self.load_data(include_features=True)
        
        # Mapeia colunas do banco para nomes originais do código
        column_mapping = {
            'ano': 'Ano',
            'ra': 'RA',
            'turma': 'Turma',
            'idade': 'Idade',
            'ano_ingresso': 'Ano ingresso',
            'fase': 'Fase',
            'instituicao_ensino': 'Instituição de ensino',
            'iaa': 'IAA',
            'ieg': 'IEG',
            'ips': 'IPS',
            'ipp': 'IPP',
            'ida': 'IDA',
            'ipv': 'IPV',
            'ian': 'IAN',
            'mat': 'Mat',
            'por': 'Por',
            'ing': 'Ing',
            'inde_22': 'INDE_22',
            'inde_23': 'INDE_23',
            'inde_24': 'INDE_24',
            'inde': 'INDE',
            'defasagem': 'Defasagem',
            'tempo_na_escola': 'Tempo_na_escola',
            'media_academica': 'Media_academica',
            'media_indicadores': 'Media_indicadores',
            'risco_defasagem': 'Risco_defasagem',
            'nivel_ian': 'Nivel_IAN'
        }
        
        # Renomeia apenas colunas que existem
        rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_dict)
        
        return df
    
    def load_data_for_modeling(self) -> pd.DataFrame:
        """
        Carrega dados formatados para modelagem.
        Retorna DataFrame com features necessárias para o modelo.
        
        Returns:
            DataFrame formatado para modelagem
        """
        df = self.load_data(include_features=True)
        
        # Seleciona colunas necessárias para o modelo
        model_columns = [
            'ano', 'ra', 'turma', 'idade', 'ano_ingresso',
            'iaa', 'ieg', 'ips', 'ipp', 'ida',
            'mat', 'por', 'ing', 'ipv',
            'instituicao_ensino', 'ian',
            'tempo_na_escola', 'media_academica', 'media_indicadores',
            'risco_defasagem'
        ]
        
        available_columns = [col for col in model_columns if col in df.columns]
        df = df[available_columns]
        
        # Mapeia para nomes originais
        column_mapping = {
            'ano': 'Ano',
            'ra': 'RA',
            'turma': 'Turma',
            'idade': 'Idade',
            'ano_ingresso': 'Ano ingresso',
            'iaa': 'IAA',
            'ieg': 'IEG',
            'ips': 'IPS',
            'ipp': 'IPP',
            'ida': 'IDA',
            'mat': 'Mat',
            'por': 'Por',
            'ing': 'Ing',
            'ipv': 'IPV',
            'instituicao_ensino': 'Instituição de ensino',
            'ian': 'IAN',
            'tempo_na_escola': 'Tempo_na_escola',
            'media_academica': 'Media_academica',
            'media_indicadores': 'Media_indicadores',
            'risco_defasagem': 'Risco_defasagem'
        }
        
        rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_dict)
        
        return df
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas gerais do banco de dados.
        
        Returns:
            Dicionário com estatísticas
        """
        conn = self.get_connection()
        
        try:
            stats = {}
            
            # Total de registros
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alunos")
            stats['total_alunos'] = cursor.fetchone()[0]
            
            # Por ano
            cursor.execute("""
                SELECT ano, COUNT(*) 
                FROM alunos 
                GROUP BY ano 
                ORDER BY ano
            """)
            stats['por_ano'] = dict(cursor.fetchall())
            
            # Distribuição de risco
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN risco_defasagem = 1 THEN 1 ELSE 0 END) as em_risco,
                    SUM(CASE WHEN risco_defasagem = 0 THEN 1 ELSE 0 END) as sem_risco
                FROM features_derivadas
            """)
            risco = cursor.fetchone()
            if risco:
                stats['risco'] = {
                    'em_risco': risco[0] or 0,
                    'sem_risco': risco[1] or 0
                }
            
            return stats
            
        finally:
            conn.close()


# Instância global (singleton pattern)
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Retorna instância global do DatabaseManager."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
