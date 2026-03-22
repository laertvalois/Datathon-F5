# Documento de Entrega — Datathon Fase 5 (FIAP)

**Atividade:** Sistema preditivo de risco de defasagem educacional — Associação Passos Mágicos  

**Curso / programa:** Pós-graduação em Data Analytics / Tech Challenge — FIAP  

**Organização parceira:** Associação Passos Mágicos  

**Data de entrega:** Março de 2026  

---

## 1. Identificação do projeto

| Campo | Informação |
|--------|------------|
| **Nome do projeto** | Passos Mágicos — Análise de risco de defasagem educacional (PEDE) |
| **Repositório GitHub** | https://github.com/laertvalois/Datathon-F5 |
| **Aplicação Streamlit (deploy)** | https://datathon-f5-grupo-49.streamlit.app/ |
| **Vídeo de apresentação** | https://www.youtube.com/watch?v=GlUnb1qd0EY |
| **Storytelling (PDF)** | Arquivo `docs/storytelling_fase5.pdf` no repositório; na app: **Início → Recursos** (visualização e download) |

---

## 2. Resumo executivo

Este trabalho entrega uma solução de **análise de dados** e **modelagem preditiva** sobre indicadores do programa **PEDE** (Programa de Educação e Desenvolvimento), utilizando a base oficial em Excel, consolidada em **SQLite**, com **EDA**, **engenharia de atributos**, comparação de modelos de **Machine Learning** e disponibilização em **aplicação web Streamlit**, respondendo às perguntas orientadoras do Datathon sobre adequação de nível, desempenho, engajamento, perfis psicossocial/psicopedagógico, ponto de virada, multidimensionalidade (INDE) e previsão de risco.

---

## 3. Entregáveis exigidos e status

| # | Entregável | Onde encontrar | Status |
|---|------------|----------------|--------|
| 1 | Código no GitHub (limpeza, análise, modelagem) | Repositório na raiz e pastas `database/`, `src/`, `utils/`, `scripts/` | Concluído |
| 2 | Apresentação / storytelling | `docs/storytelling_fase5.pdf` + aba **Recursos** na app | Concluído |
| 3 | Notebook Python com modelo preditivo | `notebooks/MODELO_PREDITIVO_DATATHON.ipynb` | Concluído |
| 4 | Aplicação Streamlit (deploy) | `app.py` — link na tabela da seção 1 | Concluído |
| 5 | Vídeo de apresentação (até ~5 min) | YouTube — link na tabela da seção 1 | Concluído |

---

## 4. Conteúdo técnico resumido

### 4.1 Dados
- **Fonte original:** `Colab/DATATHON/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`
- **Armazenamento:** `data/datathon_f5.db` (SQLite)
- **Período:** 2022, 2023 e 2024
- **Alvo do modelo:** risco de defasagem derivado do **IAN** (ex.: binário conforme implementação em `src/modelagem.py` e notebook)

### 4.2 Modelagem
- **Modelos comparados:** Regressão Logística, Random Forest, **Hist Gradient Boosting** (selecionado)
- **Pré-processamento:** imputação, escalonamento, pipeline scikit-learn
- **Divisão treino / teste:** **75% / 25%**, estratificada (`random_state` fixo para reprodutibilidade)
- **Métricas reportadas (ordem de referência):** acurácia ~92,4%, ROC-AUC ~95,7%, F1 ~92%, precision/recall da classe “em risco” conforme `DOCUMENTO_ENTREGA_FINAL.md` / `README.md`

### 4.3 Aplicação Streamlit
- **Início:** objetivo, predição, insights, informações técnicas, **recursos (inclui PDF de storytelling)**, como usar
- **Predição individual** e **Modelo preditivo** (ROC, matriz de confusão, importância de variáveis)
- **Indicadores PEDE:** IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE
- **Sobre o sistema:** autores, tecnologias, limitações

---

## 5. Estrutura principal do repositório

```
Datathon_F5/
├── app.py
├── requirements.txt
├── .streamlit/config.toml
├── data/datathon_f5.db
├── docs/storytelling_fase5.pdf
├── models/modelo_risco_defasagem.pkl
├── notebooks/MODELO_PREDITIVO_DATATHON.ipynb
├── database/          # schema + migrate_excel_to_db.py
├── src/               # analise_exploratoria.py, modelagem.py
├── utils/             # database, preprocessing, pede_calculations
├── scripts/           # pipelines executáveis
├── README.md
├── DOCUMENTO_ENTREGA_FINAL.md    # Referência técnica detalhada
└── DOCUMENTO_ENTREGA_ATIVIDADE.md # Este documento (entrega oficial resumida)
```

---

## 6. Equipe

| Nome |
|------|
| Alysson Tenório |
| Erico Leopoldino Mota |
| Henrique Bruno Oliveira Lima |
| Joao Paulo Pinheiro Aguiar |
| Laert Valois Rios Carneiro |

---

## 7. Declaração e licença

Projeto desenvolvido para fins **educacionais** no âmbito do **Datathon — Fase 5 — FIAP**, em parceria com a **Associação Passos Mágicos**.

---

## 8. Documentação complementar

Para **checklist das 11 perguntas do Datathon**, **definições dos indicadores**, **métricas completas** e **instruções de execução local**, consulte o arquivo **`DOCUMENTO_ENTREGA_FINAL.md`** no mesmo repositório.

---

**Assinatura do grupo (entrega):** documento válido como **registro de entrega da atividade**, com links e artefatos descritos acima.
