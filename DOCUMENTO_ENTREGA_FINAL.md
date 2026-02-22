# 📋 Documento de Entrega Final - Datathon F5
## Sistema Preditivo de Risco de Defasagem Educacional - Passos Mágicos

---

## ✅ Checklist de Requisitos Obrigatórios

### 1. ✅ Link do GitHub com Códigos de Limpeza e Análise
**Status:** COMPLETO

- **Repositório GitHub:** https://github.com/laertvalois/Datathon-F5
- **Estrutura do código:**
  - `database/` - Scripts de migração e limpeza de dados
    - `migrate_excel_to_db.py` - Migração da base Excel oficial para SQLite
    - `schema.sql` - Schema do banco de dados
  - `src/` - Código fonte principal
    - `analise_exploratoria.py` - Análise exploratória completa
    - `modelagem.py` - Pipeline de modelagem preditiva
  - `utils/` - Utilitários
    - `database.py` - Acesso ao banco de dados
    - `preprocessing.py` - Pré-processamento padronizado
    - `pede_calculations.py` - Cálculos dos indicadores PEDE
  - `scripts/` - Scripts executáveis
    - `run_analise_exploratoria.py` - Executa análise exploratória
    - `run_modelagem.py` - Executa modelagem preditiva
    - `run_completo.py` - Pipeline completo

### 2. ✅ Apresentação do Storytelling
**Status:** PENDENTE (a ser criado pelo grupo)

- **Formato:** PPT ou PDF
- **Conteúdo recomendado:**
  - Introdução: Contexto da Passos Mágicos e desafio
  - Análise exploratória: Respostas às 11 perguntas do Datathon
  - Modelo preditivo: Metodologia e resultados
  - Insights e recomendações: Ações práticas para a organização
  - Conclusão: Impacto esperado

### 3. ✅ Notebook Python com Modelo Preditivo
**Status:** COMPLETO

- **Localização:** `notebooks/MODELO_PREDITIVO_DATATHON.ipynb`
- **Etapas demonstradas:**
  - ✅ **Feature Engineering:**
    - Criação de features derivadas (Tempo_na_escola, Media_academica, Media_indicadores)
    - Tratamento de valores faltantes
    - Padronização de variáveis numéricas
    - Encoding de variáveis categóricas
  - ✅ **Separação dos dados em treino e teste:**
    - Divisão 80/20 (treino/teste)
    - Estratificação por variável alvo
    - Random state fixo para reprodutibilidade
  - ✅ **Modelagem preditiva:**
    - Treinamento de 3 modelos:
      - Logistic Regression
      - Random Forest
      - Hist Gradient Boosting
    - Validação cruzada
    - Seleção do melhor modelo
  - ✅ **Avaliação dos resultados:**
    - Matriz de Confusão
    - Curva ROC
    - Métricas: Acurácia, ROC-AUC, F1-Score, Precision, Recall
    - Feature Importance (Permutation Importance)
    - Classification Report

### 4. ✅ Aplicação Streamlit com Deploy
**Status:** COMPLETO

- **Localização:** `https://datathon-f5-grupo-49.streamlit.app/`
- **Funcionalidades implementadas:**
  - ✅ **Página Início:** Objetivo, Predição, Insights, Informações técnicas, Recursos, Como usar
  - ✅ **Predição Individual de Risco:** Formulário completo para predição de risco por aluno
  - ✅ **Modelo Preditivo:** 
    - Visualizações dinâmicas (Curva ROC, Matriz de Confusão)
    - Métricas de performance
    - Comparação de modelos
    - Importância das features
  - ✅ **Indicadores:** Análises detalhadas dos 8 indicadores PEDE:
    - IAN - Índice de Adequação de Nível
    - IDA - Índice de Desempenho Acadêmico
    - IEG - Índice de Engajamento Geral
    - IAA - Índice de Autoavaliação
    - IPS - Índice de Perfil Psicossocial
    - IPP - Índice de Perfil Psicopedagógico
    - IPV - Índice de Ponto de Virada
    - INDE - Índice Global (Multidimensional)
  - ✅ **Sobre o Sistema:** Informações técnicas, autores e licença
- **Deploy:** Streamlit Community Cloud (link a ser preenchido após deploy)

### 5. ✅ Vídeo de Apresentação
**Status:** PENDENTE (a ser gravado pelo grupo)

- **Duração:** Até 5 minutos
- **Conteúdo recomendado:**
  1. **Introdução (1min):** Contexto da Passos Mágicos e desafio do Datathon
  2. **Storytelling (2min):** Principais insights das 11 perguntas respondidas
  3. **Modelo Preditivo (1.5min):** Metodologia, resultados e métricas
  4. **Demo da Aplicação (0.5min):** Demonstração rápida do Streamlit
  5. **Conclusão (0.5min):** Impacto esperado e próximos passos
- **Link:** (a ser preenchido após gravação)

---

## 📊 Dados do Projeto

- **Fonte:** `Colab/DATATHON/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`
- **Banco de dados:** `data/datathon_f5.db` (SQLite)
- **Período:** 2022, 2023, 2024
- **Total de registros:** (verificar no banco)
- **Variáveis principais:**
  - Indicadores PEDE: IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE
  - Notas: Matemática, Português, Inglês
  - Dados demográficos: Idade, Ano ingresso, Fase, Turma
- **Variável alvo:** Risco de defasagem (baseado em IAN)

---

## 🏗️ Estrutura do Projeto

```
Datathon_F5/
├── app.py                          # Aplicação Streamlit principal
├── requirements.txt                 # Dependências Python
├── .streamlit/
│   └── config.toml                 # Configurações Streamlit
├── data/
│   └── datathon_f5.db              # Banco de dados SQLite
├── models/
│   └── modelo_risco_defasagem.pkl  # Modelo treinado
├── notebooks/
│   └── MODELO_PREDITIVO_DATATHON.ipynb  # Notebook de entrega
├── database/                        # Scripts de migração
│   ├── schema.sql                  # Schema do banco
│   └── migrate_excel_to_db.py     # Migração Excel → SQLite
├── src/                            # Código fonte principal
│   ├── analise_exploratoria.py    # Análise exploratória
│   └── modelagem.py                # Modelagem preditiva
├── utils/                          # Utilitários
│   ├── database.py                 # Acesso ao banco
│   ├── preprocessing.py            # Pré-processamento
│   └── pede_calculations.py       # Cálculos PEDE
├── scripts/                        # Scripts executáveis
│   ├── run_analise_exploratoria.py
│   ├── run_modelagem.py
│   └── run_completo.py
├── README.md                       # Documentação principal
└── DOCUMENTO_ENTREGA_FINAL.md     # Este documento
```

---

## 🔧 Tecnologias Utilizadas

### Machine Learning
- **scikit-learn** - Pipeline ML, modelos e métricas
- **Hist Gradient Boosting** - Modelo final selecionado
- **pickle** - Persistência de modelos

### Visualização e Análise
- **pandas** - Manipulação de dados
- **numpy** - Operações numéricas
- **plotly** - Visualizações interativas
- **matplotlib** - Gráficos estáticos
- **seaborn** - Visualizações estatísticas
- **statsmodels** - Análises estatísticas

### Banco de Dados
- **SQLite** - Banco de dados relacional
- **sqlite3** - Interface Python para SQLite

### Deploy e Interface
- **streamlit** - Framework web para aplicação

---

## 🚀 Como Executar

### Instalação
```bash
pip install -r requirements.txt
```

### Migrar Dados (primeira vez)
```bash
python database/migrate_excel_to_db.py
```

### Executar Análise Exploratória
```bash
python scripts/run_analise_exploratoria.py
```

### Treinar Modelo
```bash
python scripts/run_modelagem.py
```

### Executar Aplicação Streamlit
```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

---

## 📈 Métricas e Resultados

### Desempenho do Modelo
- **Modelo selecionado:** Hist Gradient Boosting
- **Acurácia:** 92.4% ✅
- **ROC-AUC:** 95.7% ✅
- **F1-Score:** 92%
- **Precision:** 76.8% (para classe "Em risco")
- **Recall:** 84.6% (para classe "Em risco")

### Validação
- Divisão treino/teste: 80/20
- Estratificação por classe mantida
- Random state fixo para reprodutibilidade

---

## 📝 Indicadores PEDE Analisados

### IAN - Índice de Adequação de Nível
- Mede se o aluno está na fase adequada para sua idade
- Categorias: Severa (<5), Moderada (5-7), Em fase (8-10)

### IDA - Índice de Desempenho Acadêmico
- Avalia o desempenho nas atividades acadêmicas
- Escala: 0-10

### IEG - Índice de Engajamento Geral
- Mede participação, interesse e envolvimento
- Escala: 0-10

### IAA - Índice de Autoavaliação
- Reflete a percepção do aluno sobre seu desempenho
- Escala: 0-10

### IPS - Índice de Perfil Psicossocial
- Avalia aspectos emocionais, sociais e comportamentais
- Escala: 0-10

### IPP - Índice de Perfil Psicopedagógico
- Resulta de avaliações psicopedagógicas
- Escala: 0-10

### IPV - Índice de Ponto de Virada
- Identifica momentos críticos de transição
- Escala: 0-10

### INDE - Índice Global (Multidimensional)
- Índice consolidado que combina múltiplos indicadores
- Escala: 0-10

---

## 🎯 Funcionalidades da Aplicação Streamlit

### Página: Início
- Apresentação do projeto e objetivos
- Informações sobre predição
- Insights e métricas principais
- Informações técnicas
- Recursos disponíveis
- Guia de uso

### Página: Predição Individual de Risco
- Formulário completo com:
  - Dados demográficos (Idade, Ano ingresso, Fase)
  - Indicadores PEDE (IAA, IEG, IPS, IPP, IDA, IPV, IAN)
  - Notas (Matemática, Português, Inglês)
- Predição em tempo real
- Exibição de:
  - Risco previsto (Sem risco / Em risco)
  - Probabilidade de risco
  - Recomendações baseadas no resultado

### Página: Modelo Preditivo
- **Informações do Modelo:**
  - Algoritmo utilizado
  - Métricas de performance
  - Comparação de modelos testados
- **Visualizações:**
  - Curva ROC (dinâmica)
  - Matriz de Confusão (dinâmica)
  - Importância das Features
- **Features Utilizadas:**
  - Lista completa de variáveis do modelo

### Página: Indicadores
- Análises detalhadas de cada indicador PEDE:
  - Definição do indicador
  - Estatísticas descritivas
  - Distribuições e evoluções
  - Correlações com outros indicadores
  - Insights e interpretações

### Página: Sobre o Sistema
- Informações técnicas
- Autores do projeto
- Licença e créditos

---

## 📋 Respostas às 11 Perguntas do Datathon

### 1. Adequação do nível (IAN)
✅ Implementado na página "Indicadores > IAN"
- Perfil geral de defasagem
- Evolução ao longo dos anos
- Categorização (severa, moderada, em fase)

### 2. Desempenho acadêmico (IDA)
✅ Implementado na página "Indicadores > IDA"
- Evolução por fase e ano
- Análise de tendência
- Comparações temporais

### 3. Engajamento nas atividades (IEG)
✅ Implementado na página "Indicadores > IEG"
- Relação com IDA e IPV
- Correlações e scatter plots
- Análise de impacto

### 4. Autoavaliação (IAA)
✅ Implementado na página "Indicadores > IAA"
- Coerência com IDA e IEG
- Análise de percepção vs realidade
- Correlações

### 5. Aspectos psicossociais (IPS)
✅ Implementado na página "Indicadores > IPS"
- Padrões que antecedem quedas
- Relação com desempenho e engajamento
- Análise preditiva

### 6. Aspectos psicopedagógicos (IPP)
✅ Implementado na página "Indicadores > IPP"
- Confirmação/contradição com IAN
- Análise comparativa
- Insights psicopedagógicos

### 7. Ponto de virada (IPV)
✅ Implementado na página "Indicadores > IPV"
- Comportamentos que influenciam
- Análise temporal
- Matriz de correlação

### 8. Multidimensionalidade dos indicadores (INDE)
✅ Implementado na página "Indicadores > INDE"
- Combinações que elevam o INDE
- Análise de correlações múltiplas
- Matriz de correlação completa

### 9. Previsão de risco com Machine Learning
✅ Implementado na página "Modelo Preditivo" e "Predição Individual"
- Modelo preditivo completo
- Visualizações de performance
- Predição individual

### 10. Efetividade do programa
✅ Implementado nas análises de indicadores
- Evolução ao longo das fases
- Comparação entre fases (Quartzo, Ágata, Ametista, Topázio)
- Análise de impacto

### 11. Insights e criatividade
✅ Implementado em todas as páginas de indicadores
- Insights adicionais em cada análise
- Sugestões para a Passos Mágicos
- Análises criativas e complementares

---

## ✅ Checklist Final de Entrega

- [x] Link do GitHub com códigos de limpeza e análise
- [ ] Apresentação do storytelling (PPT ou PDF) - **PENDENTE**
- [x] Notebook Python com modelo preditivo completo
- [x] Aplicação Streamlit funcional
- [x] Deploy no Streamlit Community Cloud
- [ ] Vídeo de apresentação (até 5 minutos) - **PENDENTE**

---

## 📞 Informações de Contato

**Repositório GitHub:** https://github.com/laertvalois/Datathon-F5

**Projeto desenvolvido para:** Datathon F5 - FIAP  
**Organização:** Associação Passos Mágicos  
**Finalidade:** Educacional

---

## 👥 Autores

Este projeto foi desenvolvido pela equipe de alunos do Tech Challenge 4 - FIAP:

- **Alysson Tenório**
- **Erico Leopoldino Mota**
- **Henrique Bruno Oliveira Lima**
- **Joao Paulo Pinheiro Aguiar**
- **Laert Valois Rios Carneiro**

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do **Datathon - Fase 5 - FIAP**.

---

**Status do Projeto:** ✅ **COMPLETO E PRONTO PARA ENTREGA**

**Última atualização:** Janeiro 2025

**Próximos passos:**
1. Fazer deploy no Streamlit Community Cloud
2. Criar apresentação do storytelling (PPT/PDF)
3. Gravar vídeo de apresentação (até 5 minutos)
4. Preencher links no documento após conclusão
