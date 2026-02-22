#!/usr/bin/env python
"""
Script para executar modelagem preditiva completa.
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modelagem import ModelagemPreditiva


def main():
    """Executa modelagem preditiva completa."""
    print("="*60)
    print("MODELAGEM PREDITIVA - DATATHON F5")
    print("="*60)
    
    modelagem = ModelagemPreditiva()
    resultados = modelagem.executar_pipeline_completo(
        salvar_modelo=True,
        salvar_visualizacoes=True
    )
    
    # Move visualizações para diretório correto se necessário
    import os
    import shutil
    modelagem_dir = 'output/modelagem'
    if os.path.exists('output/curva_roc.png'):
        os.makedirs(modelagem_dir, exist_ok=True)
        for file in ['curva_roc.png', 'matriz_confusao.png', 'importancia_features.png']:
            src = f'output/{file}'
            if os.path.exists(src):
                shutil.move(src, f'{modelagem_dir}/{file}')
    
    print("\n[OK] Modelagem concluida!")
    print(f"[OK] Modelo salvo em: models/modelo_risco_defasagem.pkl")
    print(f"[OK] Visualizacoes salvas em: output/modelagem/")
    
    return modelagem, resultados


if __name__ == '__main__':
    modelagem, resultados = main()
