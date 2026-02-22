#!/usr/bin/env python
"""
Script para explorar as bases de dados PEDE disponíveis.
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

def explorar_excel_2024():
    """Explora o Excel oficial de 2024."""
    print("="*60)
    print("EXPLORANDO: BASE DE DADOS PEDE 2024 - DATATHON.xlsx")
    print("="*60)
    
    excel_path = Path('Colab/Datathon/BASE DE DADOS PEDE 2024 - DATATHON.xlsx')
    
    if not excel_path.exists():
        print(f"Arquivo não encontrado: {excel_path}")
        return
    
    xls = pd.ExcelFile(str(excel_path))
    print(f"\nPlanilhas encontradas: {xls.sheet_names}")
    
    for sheet in xls.sheet_names:
        print(f"\n{'='*60}")
        print(f"PLANILHA: {sheet}")
        print("="*60)
        
        df = pd.read_excel(excel_path, sheet_name=sheet, nrows=10)
        print(f"Colunas ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\nPrimeiras 3 linhas:")
        print(df.head(3).to_string())
        
        # Verifica se tem INDE
        if 'INDE' in df.columns:
            print(f"\n✓ INDE encontrado na coluna: INDE")
            print(f"  Valores não nulos: {df['INDE'].notna().sum()}/{len(df)}")
            if df['INDE'].notna().any():
                print(f"  Range: {df['INDE'].min():.2f} - {df['INDE'].max():.2f}")
        
        # Verifica indicadores
        indicadores = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPP', 'IPV']
        presentes = [ind for ind in indicadores if ind in df.columns]
        print(f"\nIndicadores presentes: {presentes}")
        
        # Conta registros totais
        df_full = pd.read_excel(excel_path, sheet_name=sheet)
        print(f"\nTotal de registros: {len(df_full)}")


def explorar_csv_fiap():
    """Explora o CSV FIAP."""
    print("\n" + "="*60)
    print("EXPLORANDO: PEDE_PASSOS_DATASET_FIAP.csv")
    print("="*60)
    
    csv_path = Path('Colab/Datathon/Bases antigas/PEDE_PASSOS_DATASET_FIAP.csv')
    
    if not csv_path.exists():
        print(f"Arquivo não encontrado: {csv_path}")
        return
    
    # Tenta diferentes separadores
    try:
        df = pd.read_csv(csv_path, sep=';', nrows=5, encoding='utf-8')
        print("Separador: ; (ponto e vírgula)")
    except:
        try:
            df = pd.read_csv(csv_path, sep=',', nrows=5, encoding='utf-8')
            print("Separador: , (vírgula)")
        except Exception as e:
            print(f"Erro ao ler: {e}")
            return
    
    print(f"\nColunas ({len(df.columns)}):")
    for i, col in enumerate(df.columns[:20], 1):  # Primeiras 20
        print(f"  {i:2d}. {col}")
    if len(df.columns) > 20:
        print(f"  ... e mais {len(df.columns) - 20} colunas")
    
    # Conta total
    try:
        df_full = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        print(f"\nTotal de registros: {len(df_full)}")
    except:
        try:
            df_full = pd.read_csv(csv_path, sep=',', encoding='utf-8')
            print(f"\nTotal de registros: {len(df_full)}")
        except:
            print("\nNão foi possível contar registros totais")


def listar_documentos():
    """Lista documentos disponíveis."""
    print("\n" + "="*60)
    print("DOCUMENTOS DISPONIVEIS")
    print("="*60)
    
    docs_path = Path('Colab/Datathon')
    
    pdfs = list(docs_path.glob('*.pdf'))
    docxs = list(docs_path.glob('*.docx'))
    
    print("\nPDFs:")
    for pdf in pdfs:
        print(f"  - {pdf.name}")
    
    print("\nDOCX:")
    for docx in docxs:
        print(f"  - {docx.name}")


def main():
    """Função principal."""
    explorar_excel_2024()
    explorar_csv_fiap()
    listar_documentos()
    
    print("\n" + "="*60)
    print("EXPLORACAO CONCLUIDA")
    print("="*60)


if __name__ == '__main__':
    main()
