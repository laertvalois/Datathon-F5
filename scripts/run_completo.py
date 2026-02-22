#!/usr/bin/env python
"""
Script para executar pipeline completo: análise exploratória + modelagem.
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analise_exploratoria import AnaliseExploratoria
from src.modelagem import ModelagemPreditiva


def main():
    """Executa pipeline completo."""
    print("="*60)
    print("PIPELINE COMPLETO - DATATHON F5")
    print("="*60)
    
    # 1. Análise Exploratória
    print("\n[1/2] Executando análise exploratória...")
    analise = AnaliseExploratoria()
    analise.carregar_dados()
    resultados_eda = analise.gerar_relatorio()
    analise.gerar_visualizacoes(salvar=True, diretorio='output/analise_exploratoria')
    print("[OK] Analise exploratoria concluida!")
    
    # 2. Modelagem
    print("\n[2/2] Executando modelagem preditiva...")
    modelagem = ModelagemPreditiva()
    resultados_modelo = modelagem.executar_pipeline_completo(
        salvar_modelo=True,
        salvar_visualizacoes=True
    )
    print("[OK] Modelagem concluida!")
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETO CONCLUÍDO!")
    print("="*60)
    print("\nArquivos gerados:")
    print("  - Modelo: models/modelo_risco_defasagem.pkl")
    print("  - Visualizações EDA: output/analise_exploratoria/")
    print("  - Visualizações Modelo: output/modelagem/")
    
    return analise, modelagem, resultados_eda, resultados_modelo


if __name__ == '__main__':
    analise, modelagem, resultados_eda, resultados_modelo = main()
