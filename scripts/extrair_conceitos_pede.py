#!/usr/bin/env python
"""
Script para extrair e analisar conceitos do PDF PEDE.
"""

import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    print("PyPDF2 não instalado. Tentando instalar...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2
    HAS_PYPDF2 = True

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    print("pdfplumber não instalado. Tentando instalar...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    import pdfplumber
    HAS_PDFPLUMBER = True


def extrair_texto_pypdf2(caminho_pdf):
    """Extrai texto usando PyPDF2."""
    texto = ""
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao extrair com PyPDF2: {e}")
    return texto


def extrair_texto_pdfplumber(caminho_pdf):
    """Extrai texto usando pdfplumber (melhor qualidade)."""
    texto = ""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao extrair com pdfplumber: {e}")
    return texto


def analisar_conceitos_pede(texto):
    """Analisa o texto extraído procurando por conceitos PEDE."""
    conceitos = {
        'IAN': [],
        'IDA': [],
        'IEG': [],
        'IAA': [],
        'IPS': [],
        'IPP': [],
        'IPV': [],
        'INDE': [],
        'defasagem': [],
        'risco': [],
        'categorias': [],
        'escalas': []
    }
    
    linhas = texto.split('\n')
    
    # Procura por definições de indicadores
    indicadores = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPP', 'IPV', 'INDE']
    
    for i, linha in enumerate(linhas):
        linha_upper = linha.upper()
        
        # Procura por cada indicador
        for ind in indicadores:
            if ind in linha_upper:
                # Pega contexto (linha atual + próximas 3)
                contexto = '\n'.join(linhas[i:min(i+4, len(linhas))])
                conceitos[ind].append(contexto)
        
        # Procura por definições de defasagem
        if any(palavra in linha_upper for palavra in ['defasagem', 'defasado', 'adequação']):
            contexto = '\n'.join(linhas[max(0, i-2):min(i+4, len(linhas))])
            conceitos['defasagem'].append(contexto)
        
        # Procura por risco
        if 'risco' in linha_upper.lower():
            contexto = '\n'.join(linhas[max(0, i-2):min(i+4, len(linhas))])
            conceitos['risco'].append(contexto)
        
        # Procura por categorias
        if any(palavra in linha_upper for palavra in ['severa', 'moderada', 'adequado', 'em fase']):
            contexto = '\n'.join(linhas[max(0, i-2):min(i+4, len(linhas))])
            conceitos['categorias'].append(contexto)
        
        # Procura por escalas
        if any(palavra in linha_upper for palavra in ['escala', '0 a 10', '0-10', 'range']):
            contexto = '\n'.join(linhas[max(0, i-2):min(i+4, len(linhas))])
            conceitos['escalas'].append(contexto)
    
    return conceitos


def main():
    """Função principal."""
    base_dir = Path(__file__).parent.parent
    pdf_path = base_dir / 'Colab' / 'Relatório PEDE2020.pdf'
    
    if not pdf_path.exists():
        print(f"Arquivo não encontrado: {pdf_path}")
        return
    
    print("="*60)
    print("EXTRAINDO CONCEITOS DO PDF PEDE")
    print("="*60)
    print(f"Arquivo: {pdf_path}")
    
    # Tenta extrair com pdfplumber primeiro (melhor qualidade)
    print("\nTentando extrair com pdfplumber...")
    texto = extrair_texto_pdfplumber(str(pdf_path))
    
    if not texto or len(texto.strip()) < 100:
        print("pdfplumber não retornou texto suficiente. Tentando PyPDF2...")
        texto = extrair_texto_pypdf2(str(pdf_path))
    
    if not texto or len(texto.strip()) < 100:
        print("ERRO: Não foi possível extrair texto do PDF")
        return
    
    print(f"\nTexto extraído: {len(texto)} caracteres")
    
    # Analisa conceitos
    print("\nAnalisando conceitos PEDE...")
    conceitos = analisar_conceitos_pede(texto)
    
    # Salva texto completo
    output_dir = base_dir / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'texto_pede2020.txt', 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f"\nTexto completo salvo em: {output_dir / 'texto_pede2020.txt'}")
    
    # Salva análise de conceitos
    with open(output_dir / 'conceitos_pede_extraidos.md', 'w', encoding='utf-8') as f:
        f.write("# Conceitos PEDE Extraídos do PDF\n\n")
        
        for categoria, itens in conceitos.items():
            if itens:
                f.write(f"## {categoria.upper()}\n\n")
                for i, item in enumerate(set(itens[:10]), 1):  # Limita a 10 por categoria
                    f.write(f"### Item {i}\n\n")
                    f.write(f"{item}\n\n")
                    f.write("---\n\n")
    
    print(f"Análise de conceitos salva em: {output_dir / 'conceitos_pede_extraidos.md'}")
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DA EXTRAÇÃO")
    print("="*60)
    for categoria, itens in conceitos.items():
        if itens:
            print(f"{categoria}: {len(set(itens))} referências encontradas")
    
    print("\n" + "="*60)
    print("EXTRAÇÃO CONCLUÍDA!")
    print("="*60)
    print(f"\nArquivos gerados:")
    print(f"  - {output_dir / 'texto_pede2020.txt'}")
    print(f"  - {output_dir / 'conceitos_pede_extraidos.md'}")


if __name__ == '__main__':
    main()
