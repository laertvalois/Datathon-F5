# 🎓 Datathon F5 - Passos Mágicos
## Análise de Risco de Defasagem Educacional

Projeto desenvolvido para o Datathon F5, focado em análise preditiva de risco de defasagem educacional para a Associação Passos Mágicos.

---

## 📋 Sobre o Projeto

Este projeto utiliza técnicas de **Data Analytics** e **Machine Learning** para:

- Analisar indicadores educacionais (IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE)
- Identificar padrões de risco de defasagem
- Construir modelo preditivo para antecipar alunos em risco
- Disponibilizar solução via aplicação Streamlit

---

## 🏗️ Estrutura do Projeto

```
Datathon_F5/
├── src/                            # Código fonte principal
│   ├── __init__.py
│   ├── analise_exploratoria.py     # Módulo de análise exploratória
│   └── modelagem.py                # Módulo de modelagem preditiva
│
├── scripts/                        # Scripts executáveis
│   ├── __init__.py
│   ├── run_analise_exploratoria.py # Executa análise exploratória
│   ├── run_modelagem.py            # Executa modelagem
│   └── run_completo.py             # Executa pipeline completo
│
├── database/                        # Banco de dados SQLite
│   ├── schema.sql                  # Schema do banco
│   ├── migrate_csv_to_db.py        # Script de migração
│   └── README.md                   # Documentação do banco
│
├── utils/                          # Módulos utilitários
│   ├── __init__.py
│   ├── database.py                 # Acesso ao banco de dados
│   └── preprocessing.py            # Pré-processamento padronizado
│
├── data/                           # Dados (gerado após migração)
│   └── datathon_f5.db              # Banco SQLite
│
├── models/                         # Modelos treinados (gerado)
│   └── modelo_risco_defasagem.pkl
│
├── output/                         # Outputs (gerado)
│   ├── analise_exploratoria/       # Visualizações EDA
│   └── modelagem/                  # Visualizações do modelo
│
├── notebooks/                      # Notebook de entrega
│   └── MODELO_PREDITIVO_DATATHON.ipynb
│
├── Colab/                         # Notebooks originais (referência)
│   ├── TC5_Análise_Exploratória_v2.ipynb
│   └── TC5_Modelo preditivo.ipynb
│
├── app.py                         # Aplicação Streamlit
├── .streamlit/                    # Configurações Streamlit
│   └── config.toml
├── RELATORIO_ANALISE_COMPLETO.md   # Relatório de análise
├── DEPLOY.md                       # Guia de deploy
├── requirements.txt                 # Dependências
├── .gitignore                      # Arquivos ignorados pelo Git
└── README.md                       # Este arquivo
```

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Migrar Dados para SQLite

```bash
python database/migrate_csv_to_db.py
```

Isso irá:
- ✅ Criar o banco de dados em `data/datathon_f5.db`
- ✅ Carregar dados de 2022, 2023, 2024
- ✅ Padronizar e limpar dados
- ✅ Calcular features derivadas

### 3. Executar Análise Exploratória

```bash
python scripts/run_analise_exploratoria.py
```

### 4. Executar Modelagem Preditiva

```bash
python scripts/run_modelagem.py
```

### 5. Executar Pipeline Completo

```bash
python scripts/run_completo.py
```

Isso irá:
- ✅ Executar análise exploratória completa
- ✅ Treinar modelo preditivo
- ✅ Gerar visualizações
- ✅ Salvar modelo treinado

---

## 📊 Banco de Dados SQLite

### Estrutura

- **Tabela `alunos`**: Dados brutos dos alunos
- **Tabela `features_derivadas`**: Features calculadas
- **Tabela `modelos_metadata`**: Metadados dos modelos
- **Views**: `vw_alunos_completo`, `vw_analise_exploratoria`

### Acesso

```python
from utils.database import get_db_manager

db = get_db_manager()

# Para análise exploratória
df_eda = db.load_data_for_eda()

# Para modelagem
df_model = db.load_data_for_modeling()

# Estatísticas
stats = db.get_statistics()
```

Mais detalhes em: [`database/README.md`](database/README.md)

---

## 📦 Módulos do Projeto

### `src/analise_exploratoria.py`

Módulo completo de análise exploratória:

- `AnaliseExploratoria`: Classe principal
- `analisar_ian()`: Análise do IAN
- `analisar_ida()`: Análise do IDA
- `analisar_correlacoes()`: Análise de correlações
- `gerar_visualizacoes()`: Gera gráficos e visualizações
- `gerar_relatorio()`: Gera relatório completo

### `src/modelagem.py`

Módulo completo de modelagem preditiva:

- `ModelagemPreditiva`: Classe principal
- `treinar_modelos()`: Treina múltiplos modelos
- `avaliar_modelo()`: Avalia melhor modelo
- `analisar_importancia_features()`: Análise de importância
- `salvar_modelo()`: Salva modelo treinado
- `executar_pipeline_completo()`: Pipeline completo

### `utils/database.py`

Gerencia acesso ao banco de dados SQLite:

- `DatabaseManager`: Classe principal
- `get_db_manager()`: Instância singleton
- `load_data_for_eda()`: Dados para análise exploratória
- `load_data_for_modeling()`: Dados para modelagem

### `utils/preprocessing.py`

Funções padronizadas de pré-processamento:

- `preprocess_for_eda()`: Pré-processamento para EDA
- `preprocess_for_modeling()`: Pré-processamento para modelagem
- `standardize_numeric_columns()`: Padronização numérica
- `create_derived_features()`: Criação de features
- `validate_data_ranges()`: Validação de dados

---

## 📈 Modelo Preditivo

### Algoritmo

- **Melhor modelo:** Hist Gradient Boosting
- **AUC-ROC:** 0.957 (95.7%)
- **Acurácia:** 0.924 (92.4%)
- **F1-Score:** 0.92 (92%)

### Features Utilizadas

- Idade, Ano ingresso
- IAA, IEG, IPS, IPP, IDA
- Mat, Por, Ing, IPV
- Tempo_na_escola (derivada)
- Media_academica (derivada)
- Media_indicadores (derivada)

### Target

- **0:** Sem risco (IAN == 10)
- **1:** Em risco (IAN != 10)

---

## 📝 Documentação

- **[Relatório de Análise](RELATORIO_ANALISE_COMPLETO.md)**: Análise completa do trabalho realizado
- **[Plano de Migração](PLANO_MIGRACAO.md)**: Detalhes da migração para SQLite
- **[Exemplo de Atualização](EXEMPLO_ATUALIZACAO_NOTEBOOKS.md)**: Como atualizar notebooks
- **[Database README](database/README.md)**: Documentação do banco de dados

---

## 🌐 Aplicação Streamlit

### Executar Localmente

```bash
streamlit run app.py
```

A aplicação estará disponível em: `http://localhost:8501`

### Funcionalidades

- ✅ **Página Início**: Visão geral do projeto e objetivos
- ✅ **Predição Individual**: Predição de risco para um aluno específico
- ✅ **Modelo Preditivo**: Visualizações do modelo (ROC, Confusão, Importância)
- ✅ **Indicadores**: Análises detalhadas dos 8 indicadores PEDE
- ✅ **Sobre o Sistema**: Informações técnicas e créditos

### Deploy

A aplicação está pronta para deploy no Streamlit Community Cloud.

📖 **Guia completo de deploy:** [`DEPLOY.md`](DEPLOY.md)

---

## 🎯 Status do Projeto

1. ✅ Migração para SQLite (concluído)
2. ✅ Código consolidado em módulos Python (concluído)
3. ✅ Aplicação Streamlit desenvolvida (concluído)
4. ⏳ Deploy no Streamlit Community Cloud (pronto para deploy)

---

## 🔍 Análise Realizada

### Indicadores Analisados

- **IAN:** Índice de Adequação de Nível
- **IDA:** Índice de Desempenho Acadêmico
- **IEG:** Índice de Engajamento Geral
- **IAA:** Índice de Autoavaliação
- **IPS:** Índice de Perfil Psicossocial
- **IPP:** Índice de Perfil Psicopedagógico
- **IPV:** Índice de Ponto de Virada
- **INDE:** Índice Global

### Principais Insights

- IAN melhorou de 6.42 (2022) para 7.68 (2024)
- IEG tem correlação positiva moderada com IDA (0.37)
- IDA e IEG são os principais preditores de IPV
- Idade é o fator mais crítico para risco de defasagem

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Pandas, NumPy:** Manipulação de dados
- **Scikit-learn:** Machine Learning
- **SQLite:** Banco de dados
- **Plotly, Matplotlib, Seaborn:** Visualizações
- **Streamlit:** Aplicação web (a desenvolver)

---

## 📄 Licença

Este projeto foi desenvolvido para o Datathon F5.

---

## 👥 Equipe

Desenvolvido para a Associação Passos Mágicos.

---

## 📞 Contato

Para dúvidas ou sugestões, consulte a documentação ou abra uma issue.

---

**Última atualização:** 2024
