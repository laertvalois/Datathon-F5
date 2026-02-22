"""
Módulo de Análise Exploratória dos Dados
Consolida toda a análise exploratória realizada nos notebooks.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any
import warnings

from utils.database import get_db_manager
from utils.preprocessing import preprocess_for_eda

warnings.filterwarnings('ignore')


class AnaliseExploratoria:
    """Classe para realizar análise exploratória dos dados."""
    
    def __init__(self):
        """Inicializa a análise exploratória."""
        self.db = get_db_manager()
        self.df = None
        self.resultados = {}
    
    def carregar_dados(self):
        """Carrega dados do banco para análise exploratória."""
        print("Carregando dados do banco de dados...")
        self.df = self.db.load_data_for_eda()
        self.df = preprocess_for_eda(self.df)
        print(f"Dados carregados: {len(self.df)} registros")
        return self.df
    
    def analisar_ian(self) -> Dict[str, Any]:
        """
        Analisa o Índice de Adequação de Nível (IAN).
        
        Returns:
            Dicionário com resultados da análise
        """
        print("\n=== Análise do IAN (Índice de Adequação de Nível) ===")
        
        resultados = {
            'descricao': self.df['IAN'].describe().to_dict(),
            'media_anual': self.df.groupby('Ano')['IAN'].mean().to_dict(),
            'distribuicao_nivel': self.df['Nivel_IAN'].value_counts().to_dict(),
            'total_alunos': len(self.df)
        }
        
        print(f"Média geral do IAN: {self.df['IAN'].mean():.2f}")
        print(f"Desvio padrão: {self.df['IAN'].std():.2f}")
        print("\nMédia anual:")
        for ano, media in resultados['media_anual'].items():
            print(f"  {ano}: {media:.2f}")
        print("\nDistribuição por nível:")
        for nivel, count in resultados['distribuicao_nivel'].items():
            print(f"  {nivel}: {count} alunos")
        
        self.resultados['ian'] = resultados
        return resultados
    
    def analisar_ida(self) -> Dict[str, Any]:
        """
        Analisa o Índice de Desempenho Acadêmico (IDA).
        
        Returns:
            Dicionário com resultados da análise
        """
        print("\n=== Análise do IDA (Índice de Desempenho Acadêmico) ===")
        
        ida_fase_ano = self.df.groupby(['Ano', 'Fase'])['IDA'].mean().reset_index()
        
        resultados = {
            'media_geral': self.df['IDA'].mean(),
            'media_por_ano': self.df.groupby('Ano')['IDA'].mean().to_dict(),
            'media_por_fase_ano': ida_fase_ano.to_dict('records')
        }
        
        print(f"Média geral do IDA: {resultados['media_geral']:.2f}")
        print("\nMédia por ano:")
        for ano, media in resultados['media_por_ano'].items():
            print(f"  {ano}: {media:.2f}")
        
        self.resultados['ida'] = resultados
        return resultados
    
    def analisar_correlacoes(self) -> Dict[str, float]:
        """
        Analisa correlações entre indicadores.
        
        Returns:
            Dicionário com correlações calculadas
        """
        print("\n=== Análise de Correlações ===")
        
        correlacoes = {
            'IEG_IDA': self.df['IEG'].corr(self.df['IDA']),
            'IEG_IPV': self.df['IEG'].corr(self.df['IPV']),
            'IAA_IDA': self.df['IAA'].corr(self.df['IDA']),
            'IAA_IEG': self.df['IAA'].corr(self.df['IEG']),
            'IPS_IDA': self.df['IPS'].corr(self.df['IDA']),
            'IPS_IEG': self.df['IPS'].corr(self.df['IEG']),
            'IPP_IAN': self.df['IPP'].corr(self.df['IAN']),
        }
        
        # Correlações com IPV
        indicadores = ['IDA', 'IEG', 'IPS', 'IAA', 'Mat', 'Por', 'Ing']
        correlacoes_ipv = {}
        for ind in indicadores:
            if ind in self.df.columns:
                correlacoes_ipv[f'IPV_{ind}'] = self.df['IPV'].corr(self.df[ind])
        
        correlacoes.update(correlacoes_ipv)
        
        print("Correlações principais:")
        for nome, valor in sorted(correlacoes.items(), key=lambda x: abs(x[1]), reverse=True):
            print(f"  {nome}: {valor:.2f}")
        
        self.resultados['correlacoes'] = correlacoes
        return correlacoes
    
    def gerar_visualizacoes(self, salvar: bool = False, diretorio: str = 'output'):
        """
        Gera visualizações principais da análise exploratória.
        
        Args:
            salvar: Se True, salva as visualizações
            diretorio: Diretório para salvar (se salvar=True)
        """
        import os
        
        if salvar:
            os.makedirs(diretorio, exist_ok=True)
        
        # 1. Distribuição do IAN
        fig = px.histogram(
            self.df.dropna(subset=['IAN']),
            x='IAN',
            nbins=10,
            title='Distribuição do Índice de Adequação de Nível (IAN)',
            labels={'IAN': 'IAN', 'count': 'Frequência'},
            template='seaborn'
        )
        fig.update_layout(width=800, height=500)
        if salvar:
            fig.write_html(f'{diretorio}/distribuicao_ian.html')
        else:
            fig.show()
        
        # 2. Boxplot IAN por ano
        fig = px.box(
            self.df,
            x='Ano',
            y='IAN',
            title='Distribuição Anual do Índice de Adequação de Nível (IAN)',
            template='seaborn',
            points='outliers'
        )
        fig.update_layout(width=800, height=600)
        if salvar:
            fig.write_html(f'{diretorio}/ian_por_ano.html')
        else:
            fig.show()
        
        # 3. Evolução do IDA por fase e ano
        ida_fase_ano = self.df.groupby(['Ano', 'Fase'])['IDA'].mean().reset_index()
        fig = px.line(
            ida_fase_ano,
            x='Ano',
            y='IDA',
            color='Fase',
            title='Evolução do Desempenho Acadêmico Médio (IDA) por Fase e Ano'
        )
        fig.update_traces(mode='markers+lines')
        if salvar:
            fig.write_html(f'{diretorio}/ida_evolucao.html')
        else:
            fig.show()
        
        # 4. Correlação IEG vs IDA
        fig = px.scatter(
            self.df,
            x='IEG',
            y='IDA',
            trendline="ols",
            trendline_color_override="red",
            title='Relação entre Índice de Engajamento Geral (IEG) e Desempenho Acadêmico (IDA)',
            labels={'IEG': 'IEG (Engajamento)', 'IDA': 'IDA (Desempenho)'},
            template='plotly_white'
        )
        fig.update_layout(width=900, height=600)
        if salvar:
            fig.write_html(f'{diretorio}/correlacao_ieg_ida.html')
        else:
            fig.show()
        
        # 5. Matriz de correlação
        cols_corr = ['IPV', 'IPS', 'IDA', 'IEG', 'IAA', 'Mat', 'Por', 'Ing']
        df_corr = self.df[cols_corr].corr()
        
        plt.figure(figsize=(14, 8))
        sns.heatmap(df_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Mapa de Calor da Matriz de Correlação')
        if salvar:
            plt.savefig(f'{diretorio}/matriz_correlacao.png', dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
        
        print(f"\nVisualizações geradas{' e salvas' if salvar else ''}")
    
    def gerar_relatorio(self) -> Dict[str, Any]:
        """
        Gera relatório completo da análise exploratória.
        
        Returns:
            Dicionário com todos os resultados
        """
        print("\n" + "="*60)
        print("GERANDO RELATÓRIO DE ANÁLISE EXPLORATÓRIA")
        print("="*60)
        
        if self.df is None:
            self.carregar_dados()
        
        self.analisar_ian()
        self.analisar_ida()
        self.analisar_correlacoes()
        
        print("\n" + "="*60)
        print("ANÁLISE EXPLORATÓRIA CONCLUÍDA")
        print("="*60)
        
        return self.resultados


def main():
    """Função principal para executar análise exploratória."""
    analise = AnaliseExploratoria()
    analise.carregar_dados()
    resultados = analise.gerar_relatorio()
    analise.gerar_visualizacoes(salvar=True)
    
    return analise, resultados


if __name__ == '__main__':
    analise, resultados = main()
