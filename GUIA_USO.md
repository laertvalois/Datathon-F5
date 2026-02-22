# 📖 Guia de Uso - Datathon F5

Este guia explica como usar o projeto consolidado.

---

## 🚀 Início Rápido

### 1. Configuração Inicial

```bash
# Clone o repositório (ou use o projeto local)
cd Datathon_F5

# Instale as dependências
pip install -r requirements.txt
```

### 2. Migrar Dados para SQLite

**Primeira vez apenas:**

```bash
python database/migrate_csv_to_db.py
```

Isso cria o banco `data/datathon_f5.db` com todos os dados.

---

## 📊 Executando Análises

### Opção 1: Pipeline Completo (Recomendado)

Executa análise exploratória + modelagem:

```bash
python scripts/run_completo.py
```

**Saídas:**
- `models/modelo_risco_defasagem.pkl` - Modelo treinado
- `output/analise_exploratoria/` - Visualizações EDA
- `output/modelagem/` - Visualizações do modelo

### Opção 2: Análise Exploratória Apenas

```bash
python scripts/run_analise_exploratoria.py
```

**Saídas:**
- `output/analise_exploratoria/` - Visualizações e gráficos

### Opção 3: Modelagem Apenas

```bash
python scripts/run_modelagem.py
```

**Saídas:**
- `models/modelo_risco_defasagem.pkl` - Modelo treinado
- `output/modelagem/` - Visualizações do modelo

---

## 💻 Usando como Módulo Python

### Análise Exploratória

```python
from src.analise_exploratoria import AnaliseExploratoria

# Cria instância
analise = AnaliseExploratoria()

# Carrega dados
analise.carregar_dados()

# Gera relatório
resultados = analise.gerar_relatorio()

# Gera visualizações
analise.gerar_visualizacoes(salvar=True, diretorio='output/eda')
```

### Modelagem Preditiva

```python
from src.modelagem import ModelagemPreditiva

# Cria instância
modelagem = ModelagemPreditiva()

# Executa pipeline completo
resultados = modelagem.executar_pipeline_completo(
    salvar_modelo=True,
    salvar_visualizacoes=True
)

# Acessa melhor modelo
melhor_modelo = modelagem.best_model
print(f"Melhor modelo: {modelagem.best_model_name}")
```

### Usar Modelo Treinado

```python
import pickle
import pandas as pd

# Carrega modelo
with open('models/modelo_risco_defasagem.pkl', 'rb') as f:
    modelo = pickle.load(f)

# Dados de um aluno (exemplo)
aluno = {
    'Idade': 12,
    'Ano ingresso': 2019,
    'IAA': 6.8,
    'IEG': 7.0,
    'IPS': 6.5,
    'IPP': 6.9,
    'IDA': 6.7,
    'Mat': 6.0,
    'Por': 6.5,
    'Ing': 7.0,
    'IPV': 6.8,
    'Tempo_na_escola': 5,
    'Media_academica': 6.5,
    'Media_indicadores': 6.78
}

# Prepara dados
df_aluno = pd.DataFrame([aluno])

# Predição
probabilidade = modelo.predict_proba(df_aluno)[0][1]
risco = modelo.predict(df_aluno)[0]

print(f"Probabilidade de risco: {probabilidade:.2%}")
print(f"Classificação: {'Em risco' if risco == 1 else 'Sem risco'}")
```

---

## 📁 Estrutura de Arquivos Gerados

Após executar os scripts, você terá:

```
Datathon_F5/
├── data/
│   └── datathon_f5.db          # Banco de dados SQLite
│
├── models/
│   └── modelo_risco_defasagem.pkl  # Modelo treinado
│
└── output/
    ├── analise_exploratoria/
    │   ├── distribuicao_ian.html
    │   ├── ian_por_ano.html
    │   ├── ida_evolucao.html
    │   ├── correlacao_ieg_ida.html
    │   └── matriz_correlacao.png
    │
    └── modelagem/
        ├── curva_roc.png
        ├── matriz_confusao.png
        └── importancia_features.png
```

---

## 🔧 Personalização

### Alterar Parâmetros do Modelo

```python
from src.modelagem import ModelagemPreditiva

# Cria com parâmetros customizados
modelagem = ModelagemPreditiva(random_state=123)

# Altera proporção treino/teste
modelagem.preparar_dados(test_size=0.3)

# Adiciona novos modelos
modelagem.models['XGBoost'] = XGBClassifier(...)
```

### Alterar Features

```python
from src.modelagem import ModelagemPreditiva

modelagem = ModelagemPreditiva()

# Define features customizadas
modelagem.features = [
    'Idade', 'IAA', 'IEG', 'IDA',
    'Tempo_na_escola', 'Media_academica'
]

# Continua normalmente
modelagem.carregar_dados()
modelagem.preparar_dados()
```

---

## 📊 Acessando o Banco de Dados

```python
from utils.database import get_db_manager

db = get_db_manager()

# Carrega dados para EDA
df_eda = db.load_data_for_eda()

# Carrega dados para modelagem
df_model = db.load_data_for_modeling()

# Filtra por ano
df_2024 = db.load_data(years=[2024])

# Estatísticas
stats = db.get_statistics()
print(stats)
```

---

## 🐛 Troubleshooting

### Erro: "Banco de dados não encontrado"

Execute a migração:
```bash
python database/migrate_csv_to_db.py
```

### Erro: "Módulo não encontrado"

Certifique-se de estar no diretório raiz do projeto:
```bash
cd Datathon_F5
python scripts/run_completo.py
```

### Erro ao carregar modelo

Verifique se o modelo foi treinado:
```bash
python scripts/run_modelagem.py
```

---

## 📝 Notas Importantes

1. **Primeira execução:** Sempre execute a migração primeiro
2. **Re-treinar modelo:** Execute `run_modelagem.py` novamente
3. **Outputs:** Arquivos são salvos em `output/` e `models/`
4. **Banco de dados:** Fica em `data/datathon_f5.db`

---

**Pronto para usar! 🚀**
