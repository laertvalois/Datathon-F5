# 📊 Banco de Dados SQLite - Datathon F5

Este diretório contém os arquivos relacionados ao banco de dados SQLite do projeto.

## 📁 Estrutura

```
database/
├── schema.sql              # Schema do banco de dados
├── migrate_csv_to_db.py    # Script de migração CSV → SQLite
└── README.md              # Este arquivo
```

## 🚀 Como Usar

### 1. Migração Inicial dos Dados

Execute o script de migração para carregar os dados dos CSVs para o banco SQLite:

```bash
python database/migrate_csv_to_db.py
```

**Opções:**
- `--force`: Substitui dados existentes no banco

**Exemplo:**
```bash
# Migração normal
python database/migrate_csv_to_db.py

# Migração forçada (substitui dados existentes)
python database/migrate_csv_to_db.py --force
```

### 2. Localização do Banco

O banco de dados será criado em:
```
data/datathon_f5.db
```

### 3. Estrutura do Banco

#### Tabelas Principais:

- **`alunos`**: Dados brutos dos alunos
- **`features_derivadas`**: Features calculadas (Tempo_na_escola, Media_academica, etc.)
- **`modelos_metadata`**: Metadados dos modelos treinados

#### Views:

- **`vw_alunos_completo`**: View consolidada com alunos + features derivadas
- **`vw_analise_exploratoria`**: View agregada para análises exploratórias

### 4. Usando no Código

```python
from utils.database import get_db_manager

# Obtém instância do gerenciador
db = get_db_manager()

# Carrega dados para EDA
df_eda = db.load_data_for_eda()

# Carrega dados para modelagem
df_model = db.load_data_for_modeling()

# Carrega dados específicos
df_2024 = db.load_data(years=[2024])
```

## 📋 Schema Detalhado

### Tabela `alunos`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária |
| ra | TEXT | Registro do aluno |
| ano | INTEGER | Ano dos dados |
| turma | TEXT | Turma do aluno |
| idade | REAL | Idade do aluno |
| ano_ingresso | INTEGER | Ano de ingresso |
| fase | TEXT | Fase do aluno |
| instituicao_ensino | TEXT | Instituição de ensino |
| iaa, ieg, ips, ipp, ida, ipv, ian | REAL | Indicadores principais |
| mat, por, ing | REAL | Notas por disciplina |
| inde_22, inde_23, inde_24, inde | REAL | INDE por ano e consolidado |
| defasagem | TEXT | Categoria de defasagem |

### Tabela `features_derivadas`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária |
| aluno_id | INTEGER | FK para alunos |
| tempo_na_escola | INTEGER | Ano atual - Ano ingresso |
| media_academica | REAL | Média de Mat, Por, Ing |
| media_indicadores | REAL | Média de indicadores |
| risco_defasagem | INTEGER | 0 = sem risco, 1 = em risco |
| nivel_ian | TEXT | severa, moderada, em fase |

## 🔧 Manutenção

### Backup do Banco

```bash
# Windows
copy data\datathon_f5.db data\datathon_f5_backup.db

# Linux/Mac
cp data/datathon_f5.db data/datathon_f5_backup.db
```

### Verificar Integridade

```python
import sqlite3

conn = sqlite3.connect('data/datathon_f5.db')
cursor = conn.cursor()

# Verifica integridade
cursor.execute("PRAGMA integrity_check")
result = cursor.fetchone()
print(result)

conn.close()
```

## 📝 Notas

- O banco é criado automaticamente na primeira migração
- Os dados são carregados dos CSVs do GitHub
- Features derivadas são calculadas automaticamente durante a migração
- O banco é versionado junto com o código (recomendado usar Git LFS para arquivos grandes)
