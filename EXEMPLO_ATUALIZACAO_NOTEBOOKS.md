# 📝 Exemplo de Atualização dos Notebooks

Este documento mostra como atualizar os notebooks para usar o banco SQLite ao invés dos CSVs.

---

## 🔄 Notebook de Análise Exploratória

### ❌ **CÓDIGO ANTIGO (Célula 0):**

```python
# ===============================
# 1. IMPORTAÇÕES
# ===============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# ===============================
# 2. CARGA DOS DADOS
# ===============================
df_2024 = pd.read_csv('https://raw.githubusercontent.com/henriquebol/FIAP---DATATHON/refs/heads/main/data/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON%20-%20PEDE2024.csv')
df_2023 = pd.read_csv('https://raw.githubusercontent.com/henriquebol/FIAP---DATATHON/refs/heads/main/data/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON%20-%20PEDE2023.csv')
df_2022 = pd.read_csv('https://raw.githubusercontent.com/henriquebol/FIAP---DATATHON/refs/heads/main/data/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON%20-%20PEDE2022.csv')

df_2024["Ano"] = 2024
df_2023["Ano"] = 2023
df_2022["Ano"] = 2022

df_2022.rename(
    columns={'Idade 22': 'Idade', 'Matem': 'Mat', 'Portug': 'Por', 'Inglês': 'Ing'},
    inplace=True
)

# Concatenando todos os anos
df = pd.concat([df_2024, df_2023, df_2022], ignore_index=True)

df.rename(
    columns={'INDE 22':'INDE_22', 'INDE 23':'INDE_23', 'INDE 2024':'INDE_24'},
    inplace=True)
```

### ✅ **CÓDIGO NOVO (Célula 0):**

```python
# ===============================
# 1. IMPORTAÇÕES
# ===============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import warnings
import sys
from pathlib import Path

# Adiciona caminho dos utils (ajustar conforme necessário)
sys.path.append(str(Path.cwd().parent))  # Se executando do Colab, ajustar

from utils.database import get_db_manager
from utils.preprocessing import preprocess_for_eda

warnings.filterwarnings('ignore')

# ===============================
# 2. CARGA DOS DADOS DO BANCO SQLite
# ===============================
# Carrega dados já pré-processados do banco
db = get_db_manager()
df = db.load_data_for_eda()

# Aplica pré-processamento adicional se necessário
# (Features derivadas já estão calculadas no banco!)
df = preprocess_for_eda(df)

print(f"Total de registros carregados: {len(df)}")
print(f"Anos disponíveis: {sorted(df['Ano'].unique())}")
```

### 📝 **Notas:**
- ✅ Dados já vêm padronizados do banco
- ✅ Features derivadas já calculadas
- ✅ INDE já consolidado
- ✅ Nivel_IAN já criado

---

## 🔄 Notebook de Modelo Preditivo

### ❌ **CÓDIGO ANTIGO (Células 0-1):**

```python
# ===============================
# 2. CARGA DOS DADOS
# ===============================
df_2024 = pd.read_csv('https://raw.githubusercontent.com/...')
df_2023 = pd.read_csv('https://raw.githubusercontent.com/...')
df_2022 = pd.read_csv('https://raw.githubusercontent.com/...')

df_2024["Ano"] = 2024
df_2023["Ano"] = 2023
df_2022["Ano"] = 2022

df_2022.rename(
    columns={'Idade 22': 'Idade', 'Matem': 'Mat', 'Portug': 'Por', 'Inglês': 'Ing'},
    inplace=True
)

df = pd.concat([df_2024, df_2023, df_2022], ignore_index=True)

# ===============================
# 3. SELEÇÃO DE COLUNAS
# ===============================
df = df[
    ['Ano', 'RA', 'Turma', 'Idade', 'Ano ingresso',
     'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
     'Mat', 'Por', 'Ing', 'IPV',
     'Instituição de ensino', 'IAN']
]

# ===============================
# 4. CONVERSÕES E LIMPEZA
# ===============================
cols_num = df.columns
df[cols_num] = (
    df[cols_num]
    .replace(',', '.', regex=True)
    .apply(pd.to_numeric, errors='coerce')
)

df.drop_duplicates(inplace=True)

# ===============================
# 5. TARGET
# ===============================
df['Risco_defasagem'] = df['IAN'].apply(lambda x: 0 if x == 10 else 1)

# ===============================
# 6. ENGENHARIA DE ATRIBUTOS
# ===============================
df['Tempo_na_escola'] = df['Ano'] - df['Ano ingresso']
df['Media_academica'] = df[['Mat','Por','Ing']].mean(axis=1)
df['Media_indicadores'] = df[['IAA','IEG','IPS','IPP','IDA','IPV']].mean(axis=1)
```

### ✅ **CÓDIGO NOVO (Célula 0):**

```python
# ===============================
# 1. IMPORTAÇÕES
# ===============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import sys
from pathlib import Path

# Adiciona caminho dos utils
sys.path.append(str(Path.cwd().parent))

from utils.database import get_db_manager

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_auc_score,
    RocCurveDisplay
)

# ===============================
# 2. CARGA DOS DADOS DO BANCO SQLite
# ===============================
# Carrega dados já preparados para modelagem
db = get_db_manager()
df = db.load_data_for_modeling()

# Features derivadas e target já estão prontos!
# Tempo_na_escola, Media_academica, Media_indicadores, Risco_defasagem

print(f"Total de registros: {len(df)}")
print(f"Features disponíveis: {df.columns.tolist()}")
print(f"Distribuição do target:")
print(df['Risco_defasagem'].value_counts())
```

### 📝 **Notas:**
- ✅ Dados já vêm limpos e padronizados
- ✅ Features derivadas já calculadas
- ✅ Target já criado
- ✅ Duplicatas já removidas

---

## 🔧 Para Google Colab

Se estiver usando Google Colab, você precisa fazer upload dos arquivos:

### Opção 1: Upload Manual

```python
# No Colab, faça upload de:
# - utils/database.py
# - utils/preprocessing.py
# - utils/__init__.py
# - database/schema.sql (se necessário)
# - data/datathon_f5.db (banco já migrado)

from google.colab import files
files.upload()  # Selecione os arquivos

# Ajusta caminho
import sys
sys.path.append('/content')
```

### Opção 2: Clonar Repositório

```python
!git clone https://github.com/seu-usuario/Datathon_F5.git
import sys
sys.path.append('/content/Datathon_F5')

# Executa migração se necessário
!cd Datathon_F5 && python database/migrate_csv_to_db.py
```

### Opção 3: Executar Migração no Colab

```python
# Faz upload do script de migração
from google.colab import files
files.upload()  # Selecione migrate_csv_to_db.py

# Executa migração
!python migrate_csv_to_db.py

# Agora pode usar normalmente
from utils.database import get_db_manager
db = get_db_manager()
df = db.load_data_for_eda()
```

---

## ✅ Checklist de Atualização

- [ ] Executar migração: `python database/migrate_csv_to_db.py`
- [ ] Verificar criação do banco: `data/datathon_f5.db`
- [ ] Atualizar imports no notebook de EDA
- [ ] Substituir carregamento de CSV por `get_db_manager()`
- [ ] Remover código de limpeza duplicado
- [ ] Atualizar imports no notebook de modelagem
- [ ] Substituir carregamento e feature engineering
- [ ] Testar notebooks atualizados
- [ ] Validar resultados (comparar com versão anterior)

---

## 🎯 Benefícios da Atualização

✅ **Código mais limpo:** Menos linhas, mais legível  
✅ **Consistência:** Mesmos dados em todos os lugares  
✅ **Performance:** Queries SQL mais rápidas  
✅ **Manutenibilidade:** Fácil adicionar novos dados  
✅ **Preparação para Streamlit:** Base sólida pronta  

---

**Pronto para atualizar seus notebooks!** 🚀
