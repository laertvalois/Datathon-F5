#!/usr/bin/env python
"""
Script para validar cálculo do INDE conforme PEDE 2020.
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import get_db_manager
from utils.pede_calculations import calcular_inde_pede, validar_inde_calculado, documentar_ponderacoes_inde


def main():
    """Valida cálculo do INDE."""
    print("="*60)
    print("VALIDACAO DO INDE - PEDE 2020")
    print("="*60)
    
    # Carrega dados
    db = get_db_manager()
    df = db.load_data_for_eda()
    
    print(f"\nDados carregados: {len(df)} registros")
    print(f"Fases presentes: {sorted(df['Fase'].unique())}")
    
    # Calcula INDE conforme PEDE
    print("\nCalculando INDE conforme ponderacoes PEDE 2020...")
    df = calcular_inde_pede(df, fase_col='Fase')
    
    # Valida com INDE original
    print("\nValidando INDE calculado vs INDE original...")
    df = validar_inde_calculado(df, inde_original_col='INDE', inde_calculado_col='INDE_calculado')
    
    # Estatísticas
    print("\n" + "="*60)
    print("RESULTADOS DA VALIDACAO")
    print("="*60)
    
    total = len(df)
    com_inde_original = df['INDE'].notna().sum()
    com_inde_calculado = df['INDE_calculado'].notna().sum()
    comparaveis = (df['INDE'].notna() & df['INDE_calculado'].notna()).sum()
    
    print(f"\nTotal de registros: {total}")
    print(f"Com INDE original: {com_inde_original}")
    print(f"Com INDE calculado: {com_inde_calculado}")
    print(f"Comparaveis: {comparaveis}")
    
    if comparaveis > 0:
        validos = df['INDE_valido'].sum()
        print(f"INDE validos (diferenca <= 0.01): {validos}/{comparaveis} ({validos/comparaveis*100:.1f}%)")
        
        if validos < comparaveis:
            print("\nRegistros com INDE divergente:")
            divergentes = df[~df['INDE_valido'] & df['INDE_valido'].notna()]
            print(f"Total: {len(divergentes)}")
            
            if len(divergentes) > 0:
                print("\nAmostra (primeiros 5):")
                cols = ['Ano', 'Fase', 'INDE', 'INDE_calculado', 'INDE_diferenca']
                print(divergentes[cols].head().to_string())
        
        # Por fase
        print("\nValidacao por Fase:")
        for fase in sorted(df['Fase'].dropna().unique()):
            mask_fase = df['Fase'] == fase
            fase_comparaveis = (df.loc[mask_fase, 'INDE'].notna() & 
                               df.loc[mask_fase, 'INDE_calculado'].notna()).sum()
            if fase_comparaveis > 0:
                fase_validos = df.loc[mask_fase, 'INDE_valido'].sum()
                print(f"  Fase {fase}: {fase_validos}/{fase_comparaveis} validos")
    
    # Ponderações
    print("\n" + "="*60)
    print("PONDERACOES OFICIAIS PEDE 2020")
    print("="*60)
    ponderacoes = documentar_ponderacoes_inde()
    
    print("\nFases 0 a 7:")
    for ind, peso in ponderacoes['fases_0_7'].items():
        if ind != 'total':
            print(f"  {ind}: {peso*100:.0f}%")
    
    print("\nFase 8:")
    for ind, peso in ponderacoes['fase_8'].items():
        if ind != 'total':
            print(f"  {ind}: {peso*100:.0f}%")
    
    print("\n" + "="*60)
    print("VALIDACAO CONCLUIDA")
    print("="*60)


if __name__ == '__main__':
    main()
