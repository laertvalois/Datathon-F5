# 📋 Decisões do Projeto - Datathon F5

Este documento registra as decisões técnicas e metodológicas tomadas durante o desenvolvimento do projeto.

---

## 🎯 Decisão 1: Definição de Risco de Defasagem

### Decisão:
**Risco de Defasagem = 0 se IAN == 10, senão 1**

### Justificativa:
- **IAN (Índice de Adequação de Nível)** mede a adequação do aluno comparando:
  - Fase atual do aluno na Associação
  - Fase adequada para sua idade (conforme Resolução CNE)
  
- **IAN = 10** indica que o aluno está na fase adequada para sua idade → **Sem risco**
- **IAN < 10** indica defasagem (quanto menor, maior a defasagem) → **Em risco**

### Validação:
- ✅ Lógica alinhada com conceito de adequação de nível
- ✅ IAN = 10 significa adequação completa
- ⚠️ Não está explicitamente documentado no PEDE 2020, mas é inferência lógica

### Status: ✅ **Aprovada e implementada**

---

## 🎯 Decisão 2: Categorização de IAN

### Decisão:
Categorização do IAN em três níveis:
- **Severa:** IAN < 5
- **Moderada:** 5 <= IAN <= 7
- **Em fase:** IAN > 7

### Justificativa:
- Categorização útil para análises exploratórias
- Facilita interpretação dos resultados
- Permite identificar diferentes níveis de defasagem

### Validação:
- ⚠️ **Não está explicitamente no documento PEDE 2020**
- ✅ Faz sentido conceitualmente (IAN menor = maior defasagem)
- ✅ Útil para análises e visualizações

### Status: ✅ **Aprovada e implementada** (decisão do projeto)

---

## 🎯 Decisão 3: Uso da Base Oficial Excel

### Decisão:
**Migrar para base oficial Excel** (`BASE DE DADOS PEDE 2024 - DATATHON.xlsx`) ao invés dos CSVs do GitHub.

### Justificativa:
1. ✅ **Base oficial** da Passos Mágicos
2. ✅ **INDE já calculado** corretamente (não precisa recalcular)
3. ✅ **Dados mais completos** (Pedra, Destaques, Recomendações)
4. ✅ **Estrutura consistente** entre anos
5. ✅ **Dados atualizados** (2022, 2023, 2024)

### Implementação:
- Script `database/migrate_excel_to_db.py` criado
- Schema atualizado com campos novos (Pedra, Destaques, etc.)
- Migração bem-sucedida: 3.030 registros

### Status: ✅ **Implementada**

---

## 🎯 Decisão 4: Não Recalcular INDE

### Decisão:
**Usar INDE já calculado na base oficial** ao invés de recalcular.

### Justificativa:
1. ✅ INDE na base oficial já está calculado corretamente
2. ✅ Evita divergências e erros de cálculo
3. ✅ Mantém consistência com dados oficiais
4. ✅ Validação mostrou que recálculo pode ter divergências

### Implementação:
- Função `calcular_inde_pede()` criada para validação (opcional)
- Código usa INDE do banco de dados diretamente
- Não recalcula INDE no preprocessing

### Status: ✅ **Implementada**

---

## 🎯 Decisão 5: Estrutura do Banco de Dados

### Decisão:
**SQLite** como banco de dados local para:
- Consistência de dados
- Performance
- Facilidade de deploy
- Versionamento

### Estrutura:
- Tabela `alunos`: Dados principais
- Tabela `features_derivadas`: Features calculadas
- Tabela `modelos_metadata`: Metadados dos modelos
- Views para facilitar queries

### Status: ✅ **Implementada**

---

## 🎯 Decisão 6: Features do Modelo

### Features Utilizadas:
```python
features = [
    'Idade', 'Ano ingresso',
    'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
    'Mat', 'Por', 'Ing', 'IPV',
    'Tempo_na_escola',
    'Media_academica', 'Media_indicadores'
]
```

### Justificativa:
- **Indicadores PEDE:** IAN, IDA, IEG, IAA, IPS, IPP, IPV
- **Notas acadêmicas:** Mat, Por, Ing
- **Features derivadas:** Tempo_na_escola, Médias
- **IAN não incluído:** É o target (risco baseado em IAN)

### Status: ✅ **Implementada**

---

## 🎯 Decisão 7: Modelos de Machine Learning

### Modelos Testados:
1. **Logistic Regression** - Baseline
2. **Random Forest** - Boa performance, interpretável
3. **Hist Gradient Boosting** - Alta performance

### Seleção:
- Melhor modelo selecionado por **ROC-AUC**
- Uso de **class_weight='balanced'** para lidar com desbalanceamento

### Status: ✅ **Implementada**

---

## 📝 Notas Adicionais

### Sobre o PEDE:
- Documentação PEDE 2020 analisada e conceitos compreendidos
- Definições dos indicadores documentadas em `docs/DEFINICOES_PEDE.md`
- Ponderações do INDE conhecidas e validadas

### Sobre o Projeto:
- Código modularizado e organizado
- Estrutura preparada para GitHub
- Documentação completa

---

**Última atualização:** 2024
