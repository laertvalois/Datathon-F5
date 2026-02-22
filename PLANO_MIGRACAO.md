# 📋 Plano de Migração: CSV → SQLite

## ✅ O que foi criado

### 1. **Schema do Banco de Dados** (`database/schema.sql`)
- Tabela `alunos` com todos os campos
- Tabela `features_derivadas` para features calculadas
- Tabela `modelos_metadata` para versionamento de modelos
- Views para facilitar queries
- Índices para performance

### 2. **Script de Migração** (`database/migrate_csv_to_db.py`)
- Carrega dados dos CSVs do GitHub
- Padroniza e limpa dados
- Insere no banco SQLite
- Calcula features derivadas automaticamente
- Logging detalhado do processo

### 3. **Módulo de Acesso aos Dados** (`utils/database.py`)
- Classe `DatabaseManager` para abstração
- Métodos `load_data_for_eda()` e `load_data_for_modeling()`
- Mapeamento automático de colunas
- Singleton pattern para reutilização

### 4. **Módulo de Pré-processamento** (`utils/preprocessing.py`)
- Funções padronizadas de pré-processamento
- `preprocess_for_eda()` e `preprocess_for_modeling()`
- Validação de ranges
- Criação de features derivadas

## 🚀 Próximos Passos

### Passo 1: Executar Migração

```bash
# No diretório raiz do projeto
python database/migrate_csv_to_db.py
```

Isso irá:
- ✅ Criar o banco de dados em `data/datathon_f5.db`
- ✅ Carregar dados de 2022, 2023, 2024
- ✅ Padronizar e limpar dados
- ✅ Calcular features derivadas
- ✅ Criar índices e views

### Passo 2: Atualizar Notebooks

#### Notebook de Análise Exploratória

**ANTES:**
```python
df_2024 = pd.read_csv('https://raw.githubusercontent.com/...')
df_2023 = pd.read_csv('https://raw.githubusercontent.com/...')
df_2022 = pd.read_csv('https://raw.githubusercontent.com/...')
# ... código de limpeza ...
```

**DEPOIS:**
```python
import sys
sys.path.append('..')  # Se executando do Colab, ajustar caminho

from utils.database import get_db_manager
from utils.preprocessing import preprocess_for_eda

# Carrega dados do banco
db = get_db_manager()
df = db.load_data_for_eda()

# Aplica pré-processamento padronizado (se necessário)
df = preprocess_for_eda(df)
```

#### Notebook de Modelo Preditivo

**ANTES:**
```python
df_2024 = pd.read_csv('https://raw.githubusercontent.com/...')
# ... código de limpeza e feature engineering ...
```

**DEPOIS:**
```python
import sys
sys.path.append('..')

from utils.database import get_db_manager
from utils.preprocessing import preprocess_for_modeling

# Carrega dados do banco
db = get_db_manager()
df = db.load_data_for_modeling()

# Features derivadas já estão calculadas no banco!
# Target já está criado!
```

### Passo 3: Testar Migração

```python
from utils.database import get_db_manager

db = get_db_manager()

# Testa carregamento
df_eda = db.load_data_for_eda()
print(f"Registros para EDA: {len(df_eda)}")
print(df_eda.head())

df_model = db.load_data_for_modeling()
print(f"Registros para modelagem: {len(df_model)}")
print(df_model.head())

# Estatísticas
stats = db.get_statistics()
print(stats)
```

## 📊 Vantagens da Migração

### ✅ **Consistência**
- Uma única fonte de verdade
- Pré-processamento padronizado
- Features derivadas calculadas uma vez

### ✅ **Performance**
- Queries SQL são mais rápidas que ler CSVs
- Índices otimizam buscas
- Cache de conexão

### ✅ **Facilidade para Streamlit**
- Conexão direta ao banco
- Queries filtradas por ano/turma/fase
- Dados sempre atualizados

### ✅ **Manutenibilidade**
- Schema versionado
- Migrações controladas
- Backup simples

## 🔧 Ajustes Necessários

### 1. **Caminhos no Colab**

Se executando no Google Colab, você precisará:

```python
# Fazer upload dos arquivos utils/ e database/
# Ou clonar o repositório no Colab

# Exemplo:
!git clone https://github.com/seu-repo/Datathon_F5.git
import sys
sys.path.append('/content/Datathon_F5')
```

### 2. **Banco de Dados no Colab**

Para usar no Colab, você pode:

**Opção A:** Fazer upload do banco gerado localmente
```python
from google.colab import files
files.upload()  # Upload datathon_f5.db
```

**Opção B:** Executar migração no Colab
```python
# Executar migrate_csv_to_db.py no Colab
!python database/migrate_csv_to_db.py
```

### 3. **Compatibilidade com Código Existente**

O código existente continua funcionando! Os métodos retornam DataFrames com os mesmos nomes de colunas que o código original espera.

## 📝 Checklist de Migração

- [ ] Executar `migrate_csv_to_db.py`
- [ ] Verificar criação do banco em `data/datathon_f5.db`
- [ ] Testar carregamento de dados
- [ ] Atualizar notebook de EDA
- [ ] Atualizar notebook de modelagem
- [ ] Testar notebooks atualizados
- [ ] Validar resultados (comparar com versão anterior)
- [ ] Documentar mudanças

## 🎯 Resultado Esperado

Após a migração, você terá:

1. ✅ Banco de dados SQLite com todos os dados
2. ✅ Código padronizado e reutilizável
3. ✅ Pré-processamento consistente
4. ✅ Base sólida para aplicação Streamlit
5. ✅ Facilidade para adicionar novos dados

---

**Pronto para começar? Execute a migração e vamos atualizar os notebooks!** 🚀
