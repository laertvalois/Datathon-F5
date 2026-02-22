# 📁 Estrutura do Projeto - Datathon F5

Documentação completa da estrutura do projeto consolidado.

---

## 🗂️ Estrutura de Diretórios

```
Datathon_F5/
│
├── 📂 src/                          # Código fonte principal
│   ├── __init__.py                  # Inicialização do módulo
│   ├── analise_exploratoria.py     # Módulo de análise exploratória
│   └── modelagem.py                # Módulo de modelagem preditiva
│
├── 📂 scripts/                      # Scripts executáveis
│   ├── __init__.py
│   ├── run_analise_exploratoria.py # Executa análise exploratória
│   ├── run_modelagem.py            # Executa modelagem
│   └── run_completo.py             # Executa pipeline completo
│
├── 📂 database/                     # Banco de dados SQLite
│   ├── schema.sql                  # Schema do banco
│   ├── migrate_csv_to_db.py        # Script de migração CSV → SQLite
│   └── README.md                   # Documentação do banco
│
├── 📂 utils/                        # Módulos utilitários
│   ├── __init__.py
│   ├── database.py                 # Gerenciador de acesso ao banco
│   └── preprocessing.py            # Funções de pré-processamento
│
├── 📂 data/                         # Dados (gerado)
│   └── datathon_f5.db              # Banco SQLite
│
├── 📂 models/                       # Modelos treinados (gerado)
│   └── modelo_risco_defasagem.pkl  # Modelo preditivo
│
├── 📂 output/                       # Outputs gerados (gerado)
│   ├── analise_exploratoria/       # Visualizações EDA
│   └── modelagem/                  # Visualizações do modelo
│
├── 📂 Colab/                        # Notebooks originais (referência)
│   ├── TC5_Análise_Exploratória_v2.ipynb
│   └── TC5_Modelo preditivo.ipynb
│
├── 📄 README.md                     # Documentação principal
├── 📄 GUIA_USO.md                  # Guia de uso detalhado
├── 📄 ESTRUTURA_PROJETO.md         # Este arquivo
├── 📄 RELATORIO_ANALISE_COMPLETO.md # Relatório de análise
├── 📄 requirements.txt              # Dependências Python
└── 📄 .gitignore                    # Arquivos ignorados pelo Git
```

---

## 📦 Módulos Principais

### `src/analise_exploratoria.py`

**Classe:** `AnaliseExploratoria`

**Métodos principais:**
- `carregar_dados()` - Carrega dados do banco
- `analisar_ian()` - Análise do IAN
- `analisar_ida()` - Análise do IDA
- `analisar_correlacoes()` - Análise de correlações
- `gerar_visualizacoes()` - Gera visualizações
- `gerar_relatorio()` - Gera relatório completo

**Uso:**
```python
from src.analise_exploratoria import AnaliseExploratoria

analise = AnaliseExploratoria()
analise.carregar_dados()
resultados = analise.gerar_relatorio()
```

### `src/modelagem.py`

**Classe:** `ModelagemPreditiva`

**Métodos principais:**
- `carregar_dados()` - Carrega dados do banco
- `preparar_dados()` - Separa treino/teste
- `treinar_modelos()` - Treina múltiplos modelos
- `avaliar_modelo()` - Avalia melhor modelo
- `analisar_importancia_features()` - Análise de importância
- `salvar_modelo()` - Salva modelo treinado
- `executar_pipeline_completo()` - Pipeline completo

**Uso:**
```python
from src.modelagem import ModelagemPreditiva

modelagem = ModelagemPreditiva()
resultados = modelagem.executar_pipeline_completo()
```

### `utils/database.py`

**Classe:** `DatabaseManager`

**Métodos principais:**
- `load_data_for_eda()` - Dados para análise exploratória
- `load_data_for_modeling()` - Dados para modelagem
- `load_data()` - Dados customizados
- `get_statistics()` - Estatísticas do banco

**Uso:**
```python
from utils.database import get_db_manager

db = get_db_manager()
df = db.load_data_for_eda()
```

### `utils/preprocessing.py`

**Funções principais:**
- `preprocess_for_eda()` - Pré-processamento para EDA
- `preprocess_for_modeling()` - Pré-processamento para modelagem
- `standardize_numeric_columns()` - Padronização numérica
- `create_derived_features()` - Criação de features
- `validate_data_ranges()` - Validação de dados

**Uso:**
```python
from utils.preprocessing import preprocess_for_eda

df = preprocess_for_eda(df)
```

---

## 🚀 Scripts Executáveis

### `scripts/run_analise_exploratoria.py`

Executa análise exploratória completa.

**Comando:**
```bash
python scripts/run_analise_exploratoria.py
```

**Saídas:**
- `output/analise_exploratoria/` - Visualizações HTML e PNG

### `scripts/run_modelagem.py`

Executa modelagem preditiva completa.

**Comando:**
```bash
python scripts/run_modelagem.py
```

**Saídas:**
- `models/modelo_risco_defasagem.pkl` - Modelo treinado
- `output/modelagem/` - Visualizações do modelo

### `scripts/run_completo.py`

Executa pipeline completo (EDA + Modelagem).

**Comando:**
```bash
python scripts/run_completo.py
```

**Saídas:**
- Todos os outputs acima

---

## 🗄️ Banco de Dados

### Estrutura

**Tabelas:**
- `alunos` - Dados brutos dos alunos
- `features_derivadas` - Features calculadas
- `modelos_metadata` - Metadados dos modelos

**Views:**
- `vw_alunos_completo` - View consolidada
- `vw_analise_exploratoria` - View para análises

### Migração

**Script:** `database/migrate_csv_to_db.py`

**Comando:**
```bash
python database/migrate_csv_to_db.py
```

**Opções:**
- `--force` - Substitui dados existentes

---

## 📊 Fluxo de Dados

```
CSVs do GitHub
    ↓
[database/migrate_csv_to_db.py]
    ↓
SQLite (data/datathon_f5.db)
    ↓
[utils/database.py]
    ↓
DataFrames Python
    ↓
[src/analise_exploratoria.py]  ou  [src/modelagem.py]
    ↓
Resultados e Visualizações
```

---

## 🔄 Fluxo de Execução

### Pipeline Completo

1. **Migração** (primeira vez):
   ```bash
   python database/migrate_csv_to_db.py
   ```

2. **Análise Exploratória**:
   ```bash
   python scripts/run_analise_exploratoria.py
   ```

3. **Modelagem**:
   ```bash
   python scripts/run_modelagem.py
   ```

   Ou tudo de uma vez:
   ```bash
   python scripts/run_completo.py
   ```

---

## 📝 Arquivos de Configuração

### `requirements.txt`

Lista todas as dependências Python do projeto.

**Instalação:**
```bash
pip install -r requirements.txt
```

### `.gitignore`

Define arquivos ignorados pelo Git:
- `__pycache__/`
- `*.pyc`
- `data/*.db`
- `models/*.pkl`
- `output/`

---

## 📚 Documentação

### Documentação Principal

- **README.md** - Visão geral do projeto
- **GUIA_USO.md** - Guia de uso detalhado
- **ESTRUTURA_PROJETO.md** - Este arquivo

### Documentação Técnica

- **RELATORIO_ANALISE_COMPLETO.md** - Relatório de análise
- **database/README.md** - Documentação do banco

---

## ✅ Checklist para GitHub

Antes de fazer commit:

- [ ] Executar `python database/migrate_csv_to_db.py` (criar banco)
- [ ] Executar `python scripts/run_completo.py` (gerar outputs)
- [ ] Verificar que `.gitignore` está correto
- [ ] Verificar que `requirements.txt` está atualizado
- [ ] Verificar que README.md está atualizado
- [ ] Testar que scripts executam corretamente

**Nota:** O banco de dados (`data/datathon_f5.db`) pode ser grande. Considere usar Git LFS ou documentar como gerar o banco.

---

**Estrutura organizada e pronta para GitHub! 🚀**
