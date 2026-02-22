#!/usr/bin/env python
"""
Script para executar análise exploratória completa.
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analise_exploratoria import AnaliseExploratoria


def main():
    """Executa análise exploratória completa."""
    print("="*60)
    print("ANÁLISE EXPLORATÓRIA - DATATHON F5")
    print("="*60)
    
    analise = AnaliseExploratoria()
    analise.carregar_dados()
    resultados = analise.gerar_relatorio()
    analise.gerar_visualizacoes(salvar=True, diretorio='output/analise_exploratoria')
    
    print("\n[OK] Analise exploratoria concluida!")
    print(f"[OK] Resultados salvos em: output/analise_exploratoria/")
    
    return analise, resultados


if __name__ == '__main__':
    analise, resultados = main()
