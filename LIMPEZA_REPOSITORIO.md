# 🧹 Plano de Limpeza do Repositório

## Arquivos a MANTER (Essenciais para Entrega)

### Código Fonte
- ✅ `app.py` - Aplicação Streamlit
- ✅ `requirements.txt` - Dependências
- ✅ `.streamlit/config.toml` - Configurações Streamlit
- ✅ `src/` - Código fonte principal
- ✅ `utils/` - Utilitários
- ✅ `database/` - Scripts de migração e limpeza
- ✅ `scripts/` - Scripts executáveis

### Dados e Modelos
- ✅ `data/datathon_f5.db` - Banco de dados
- ✅ `models/modelo_risco_defasagem.pkl` - Modelo treinado

### Notebook de Entrega
- ✅ `notebooks/MODELO_PREDITIVO_DATATHON.ipynb` - Notebook obrigatório

### Documentação Essencial
- ✅ `README.md` - Documentação principal
- ✅ `DOCUMENTO_ENTREGA_FINAL.md` - Documento de entrega
- ✅ `DEPLOY.md` - Guia de deploy (útil)

### Referência (Opcional)
- ⚠️ `Colab/TC5_Análise_Exploratória_v2.ipynb` - Notebook original (referência)
- ⚠️ `Colab/TC5_Modelo preditivo.ipynb` - Notebook original (referência)
- ⚠️ `Colab/BASE DE DADOS PEDE 2024 - DATATHON.xlsx` - Base oficial (referência)

---

## Arquivos a REMOVER (Documentação Excessiva)

### Documentação de Processo (Remover)
- ❌ `ALINHAMENTO_PEDE.md`
- ❌ `ANALISE_ALINHAMENTO_PEDE.md`
- ❌ `ANALISE_PEDE_SITUACAO.md`
- ❌ `COMPARACAO_NOTEBOOKS_STREAMLIT.md`
- ❌ `CONCLUSAO_ALINHAMENTO_PEDE.md`
- ❌ `ESTRUTURA_PROJETO.md`
- ❌ `EXEMPLO_ATUALIZACAO_NOTEBOOKS.md`
- ❌ `GUIA_USO.md`
- ❌ `MIGRACAO_CONCLUIDA.md`
- ❌ `PLANO_ENTREGA_DATATHON.md`
- ❌ `PLANO_MIGRACAO.md`
- ❌ `PROGRESSO_EXECUCAO.md`
- ❌ `PROXIMOS_PASSOS_ATUALIZADO.md`
- ❌ `PROXIMOS_PASSOS.md`
- ❌ `RELATORIO_ANALISE_COMPLETO.md` (manter apenas se necessário)
- ❌ `RELATORIO_ANALISE_COMPLETO.txt`
- ❌ `RELATORIO_ANALISE_TEMPLATE.md`
- ❌ `RESUMO_ALINHAMENTO_PEDE.md`
- ❌ `RESUMO_BASES_PEDE.md`
- ❌ `RESUMO_MIGRACAO_SQLITE.md`
- ❌ `RESUMO_PREPARACAO_DEPLOY.md`
- ❌ `RESUMO_PROXIMOS_PASSOS.md`
- ❌ `TESTES_REALIZADOS.md`
- ❌ `VERIFICACAO_APROVEITAMENTO.md`
- ❌ `VERIFICACAO_CONCEITOS_PEDE.md`
- ❌ `LIMPEZA_REPOSITORIO.md` (este arquivo, após limpeza)

### Documentação Técnica (Opcional - pode manter)
- ⚠️ `docs/DECISOES_PROJETO.md` (manter se útil)
- ⚠️ `docs/DEFINICOES_PEDE.md` (manter se útil)

### Outros
- ❌ `🧑‍💻 Seu Papel-analista de dados.txt` - Arquivo de configuração pessoal

---

## Estrutura Final do Repositório

```
Datathon_F5/
├── app.py                          # ✅ Aplicação Streamlit
├── requirements.txt                 # ✅ Dependências
├── .streamlit/
│   └── config.toml                 # ✅ Configurações
├── .gitignore                      # ✅ Git ignore
├── data/
│   └── datathon_f5.db              # ✅ Banco de dados
├── models/
│   └── modelo_risco_defasagem.pkl  # ✅ Modelo treinado
├── notebooks/
│   └── MODELO_PREDITIVO_DATATHON.ipynb  # ✅ Notebook de entrega
├── database/                        # ✅ Scripts de migração
│   ├── schema.sql
│   ├── migrate_excel_to_db.py
│   └── README.md
├── src/                            # ✅ Código fonte
│   ├── __init__.py
│   ├── analise_exploratoria.py
│   └── modelagem.py
├── utils/                          # ✅ Utilitários
│   ├── __init__.py
│   ├── database.py
│   ├── preprocessing.py
│   └── pede_calculations.py
├── scripts/                        # ✅ Scripts executáveis
│   ├── __init__.py
│   ├── run_analise_exploratoria.py
│   ├── run_modelagem.py
│   └── run_completo.py
├── README.md                       # ✅ Documentação principal
├── DOCUMENTO_ENTREGA_FINAL.md     # ✅ Documento de entrega
├── DEPLOY.md                       # ✅ Guia de deploy
└── Colab/                          # ⚠️ Referência (opcional)
    ├── TC5_Análise_Exploratória_v2.ipynb
    ├── TC5_Modelo preditivo.ipynb
    └── BASE DE DADOS PEDE 2024 - DATATHON.xlsx
```

---

## Comandos para Limpeza

```bash
# Remover arquivos de documentação excessiva
git rm ALINHAMENTO_PEDE.md
git rm ANALISE_ALINHAMENTO_PEDE.md
git rm ANALISE_PEDE_SITUACAO.md
git rm COMPARACAO_NOTEBOOKS_STREAMLIT.md
git rm CONCLUSAO_ALINHAMENTO_PEDE.md
git rm ESTRUTURA_PROJETO.md
git rm EXEMPLO_ATUALIZACAO_NOTEBOOKS.md
git rm GUIA_USO.md
git rm MIGRACAO_CONCLUIDA.md
git rm PLANO_ENTREGA_DATATHON.md
git rm PLANO_MIGRACAO.md
git rm PROGRESSO_EXECUCAO.md
git rm PROXIMOS_PASSOS_ATUALIZADO.md
git rm PROXIMOS_PASSOS.md
git rm RELATORIO_ANALISE_COMPLETO.txt
git rm RELATORIO_ANALISE_TEMPLATE.md
git rm RESUMO_ALINHAMENTO_PEDE.md
git rm RESUMO_BASES_PEDE.md
git rm RESUMO_MIGRACAO_SQLITE.md
git rm RESUMO_PREPARACAO_DEPLOY.md
git rm RESUMO_PROXIMOS_PASSOS.md
git rm TESTES_REALIZADOS.md
git rm VERIFICACAO_APROVEITAMENTO.md
git rm VERIFICACAO_CONCEITOS_PEDE.md
git rm "🧑‍💻 Seu Papel-analista de dados.txt"

# Commit
git commit -m "Limpar repositório: remover documentação excessiva, manter apenas arquivos essenciais"

# Push
git push origin main
```
