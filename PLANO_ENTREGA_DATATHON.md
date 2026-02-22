# 🎯 Plano de Entrega - Datathon Passos Mágicos

## 📋 Requisitos do Datathon

### Entregas Obrigatórias:
1. ✅ **Link do GitHub** com códigos de limpeza e análise
2. ✅ **Apresentação** do storytelling (PPT ou PDF)
3. ✅ **Notebook Python** com modelo preditivo demonstrando:
   - Feature engineering
   - Separação treino/teste
   - Modelagem preditiva
   - Avaliação dos resultados
4. ✅ **Aplicação Streamlit** para disponibilizar modelo treinado
   - Deploy no Streamlit Community Cloud
5. ✅ **Vídeo** de até 5 minutos apresentando resultados

---

## 🔍 Situação Atual

### ✅ O que já temos:
1. **Análise Exploratória** - Notebook e código refatorado
2. **Modelo Preditivo** - Notebook e código refatorado
3. **Estrutura de Projeto** - Organizada para GitHub
4. **Banco de Dados SQLite** - Estrutura criada
5. **Documentação PEDE** - Conceitos e definições conhecidos
6. **Base Oficial Excel** - Identificada e disponível

### ⚠️ Falhas Identificadas:
1. **Base de dados** - Usando CSVs do GitHub ao invés da base oficial Excel
2. **INDE** - Tentando recalcular quando já está calculado na base oficial
3. **Definição de Risco** - Precisa validação (IAN == 10 = sem risco?)
4. **Categorização IAN** - Não está no PEDE oficial
5. **Estrutura de dados** - Pode ser melhorada com base oficial

---

## 🎯 Plano de Ação - Próximos Passos

### **FASE 1: Migração para Base Oficial** ⏱️ Prioridade ALTA

#### 1.1 Criar Script de Migração Excel → SQLite
**Arquivo:** `database/migrate_excel_to_db.py`

**Objetivos:**
- Ler base oficial Excel (`BASE DE DADOS PEDE 2024 - DATATHON.xlsx`)
- Migrar dados das 3 planilhas (2022, 2023, 2024)
- Usar INDE já calculado (não recalcular)
- Padronizar estrutura mantendo compatibilidade
- Preservar campos adicionais (Pedra, Destaques, etc.)

**Ações:**
- [ ] Criar função para ler Excel oficial
- [ ] Padronizar colunas entre anos (2022, 2023, 2024)
- [ ] Mapear para estrutura do banco SQLite
- [ ] Usar INDE já calculado (INDE 22, INDE 23, INDE 2024)
- [ ] Manter compatibilidade com código existente
- [ ] Testar migração completa

**Resultado:** Banco SQLite atualizado com base oficial

---

#### 1.2 Atualizar Estrutura do Banco
**Arquivo:** `database/schema.sql`

**Objetivos:**
- Adicionar campos novos da base oficial
- Manter compatibilidade com código existente
- Incluir histórico de INDE

**Campos a adicionar:**
- `pedra_20`, `pedra_21`, `pedra_22`, `pedra_23`, `pedra_24`
- `destaque_ieg`, `destaque_ida`, `destaque_ipv`
- `fase_ideal`, `defasagem` (já existe como `defasagem`)
- `inde_22`, `inde_23`, `inde_24` (histórico)

**Ações:**
- [ ] Atualizar schema.sql
- [ ] Adicionar campos opcionais
- [ ] Criar views atualizadas
- [ ] Testar compatibilidade

---

### **FASE 2: Correções e Validações** ⏱️ Prioridade ALTA

#### 2.1 Validar Definição de Risco
**Arquivo:** `utils/preprocessing.py`

**Objetivos:**
- Validar se `IAN == 10` realmente significa "sem risco"
- Documentar decisão
- Ajustar se necessário

**Ações:**
- [ ] Analisar distribuição de IAN
- [ ] Verificar lógica: IAN == 10 = sem risco
- [ ] Documentar decisão em `docs/DECISOES_PROJETO.md`
- [ ] Ajustar código se necessário

**Resultado:** Definição de risco validada e documentada

---

#### 2.2 Validar Categorização de IAN
**Arquivo:** `utils/preprocessing.py` (função `create_nivel_ian`)

**Objetivos:**
- Verificar origem das categorias (severa/moderada/em fase)
- Documentar se não estiver no PEDE oficial
- Manter se fizer sentido conceitualmente

**Ações:**
- [ ] Verificar se categorias estão em documentação PEDE
- [ ] Se não estiver, documentar como decisão do projeto
- [ ] Manter categorização se fizer sentido
- [ ] Documentar em `docs/DECISOES_PROJETO.md`

**Resultado:** Categorização validada e documentada

---

#### 2.3 Atualizar Preprocessing
**Arquivo:** `utils/preprocessing.py`

**Objetivos:**
- Usar INDE da base oficial (não recalcular)
- Manter compatibilidade com código existente
- Ajustar para novos campos

**Ações:**
- [ ] Remover cálculo de INDE (usar do banco)
- [ ] Ajustar funções de pré-processamento
- [ ] Manter features derivadas
- [ ] Testar compatibilidade

---

### **FASE 3: Re-treinar Modelo** ⏱️ Prioridade MÉDIA

#### 3.1 Re-treinar com Base Oficial
**Arquivo:** `src/modelagem.py`

**Objetivos:**
- Re-treinar modelo com base oficial
- Validar performance
- Comparar com modelo anterior

**Ações:**
- [ ] Executar pipeline completo com base oficial
- [ ] Comparar métricas com modelo anterior
- [ ] Validar se performance melhorou
- [ ] Salvar novo modelo

**Resultado:** Modelo re-treinado com base oficial

---

### **FASE 4: Notebook de Entrega** ⏱️ Prioridade ALTA

#### 4.1 Criar Notebook Consolidado
**Arquivo:** `notebooks/MODELO_PREDITIVO_DATATHON.ipynb`

**Objetivos:**
- Criar notebook único para entrega
- Demonstrar todas as etapas exigidas
- Manter storytelling e análises

**Estrutura do Notebook:**
1. **Introdução e Contexto**
2. **Carregamento de Dados** (base oficial)
3. **Análise Exploratória** (resumo)
4. **Feature Engineering**
   - Features derivadas
   - Tratamento de missing
   - Normalização
5. **Separação Treino/Teste**
6. **Modelagem Preditiva**
   - Múltiplos modelos
   - Seleção do melhor
7. **Avaliação dos Resultados**
   - Métricas (Accuracy, ROC-AUC)
   - Matriz de confusão
   - Curva ROC
   - Importância de features
8. **Conclusões e Insights**

**Ações:**
- [ ] Criar notebook baseado em `src/modelagem.py`
- [ ] Incluir visualizações principais
- [ ] Adicionar markdown explicativo
- [ ] Garantir que todas as etapas estão demonstradas
- [ ] Testar execução completa

**Resultado:** Notebook pronto para entrega

---

### **FASE 5: Aplicação Streamlit** ⏱️ Prioridade ALTA

#### 5.1 Estrutura da Aplicação
**Arquivo:** `app.py` (raiz do projeto)

**Funcionalidades:**
1. **Página Inicial**
   - Apresentação do projeto
   - Contexto Passos Mágicos
   - Objetivo da aplicação

2. **Predição Individual**
   - Formulário para entrada de dados do aluno
   - Campos: Idade, Ano ingresso, IAA, IEG, IPS, IPP, IDA, Mat, Por, Ing, IPV
   - Botão de predição
   - Exibição de resultado:
     - Probabilidade de risco
     - Classificação (Em risco / Sem risco)
     - Gráfico de probabilidade
     - Recomendações baseadas no resultado

3. **Análise de Dados**
   - Dashboard com visualizações principais
   - Distribuições dos indicadores
   - Correlações
   - Evolução temporal

4. **Sobre o Modelo**
   - Informações sobre o modelo treinado
   - Métricas de performance
   - Importância das features
   - Metodologia

**Ações:**
- [ ] Criar estrutura básica do Streamlit
- [ ] Implementar página de predição individual
- [ ] Criar dashboard de análises
- [ ] Adicionar visualizações interativas
- [ ] Implementar carregamento do modelo
- [ ] Adicionar tratamento de erros
- [ ] Melhorar UI/UX

**Resultado:** Aplicação Streamlit funcional

---

#### 5.2 Integração com Modelo
**Arquivo:** `app.py`

**Objetivos:**
- Carregar modelo treinado
- Aplicar mesmo pré-processamento
- Fazer predições em tempo real

**Ações:**
- [ ] Criar função para carregar modelo
- [ ] Implementar pré-processamento no Streamlit
- [ ] Criar função de predição
- [ ] Adicionar validação de inputs
- [ ] Testar predições

---

#### 5.3 Visualizações Interativas
**Arquivo:** `app.py` ou `utils/visualizations.py`

**Objetivos:**
- Gráficos interativos (Plotly)
- Dashboard responsivo
- Visualizações úteis para Passos Mágicos

**Visualizações:**
- Distribuição de risco
- Importância de features
- Correlações entre indicadores
- Evolução temporal (se aplicável)

---

### **FASE 6: Deploy Streamlit** ⏱️ Prioridade ALTA

#### 6.1 Preparar para Deploy
**Arquivo:** `.streamlit/config.toml` (se necessário)

**Objetivos:**
- Configurar aplicação para deploy
- Garantir que todos os arquivos necessários estão incluídos
- Testar localmente antes do deploy

**Arquivos necessários:**
- `app.py`
- `models/modelo_risco_defasagem.pkl`
- `requirements.txt` (atualizado)
- `README.md` (com instruções de deploy)

**Ações:**
- [ ] Criar `.streamlit/config.toml` (se necessário)
- [ ] Atualizar `requirements.txt` com Streamlit
- [ ] Testar aplicação localmente
- [ ] Preparar instruções de deploy
- [ ] Criar arquivo `packages.txt` (se necessário)

---

#### 6.2 Deploy no Streamlit Community Cloud
**Objetivos:**
- Fazer deploy da aplicação
- Testar em produção
- Garantir que está funcionando

**Ações:**
- [ ] Conectar repositório GitHub ao Streamlit Cloud
- [ ] Configurar variáveis de ambiente (se necessário)
- [ ] Fazer deploy
- [ ] Testar todas as funcionalidades
- [ ] Validar performance

**Resultado:** Aplicação disponível online

---

### **FASE 7: Documentação Final** ⏱️ Prioridade MÉDIA

#### 7.1 Atualizar README.md
**Arquivo:** `README.md`

**Conteúdo:**
- Descrição do projeto
- Instruções de instalação
- Como executar análises
- Como usar a aplicação Streamlit
- Link para deploy
- Estrutura do projeto

**Ações:**
- [ ] Atualizar README com informações completas
- [ ] Adicionar screenshots da aplicação
- [ ] Incluir link do deploy
- [ ] Documentar estrutura do projeto

---

#### 7.2 Criar Documentação de Decisões
**Arquivo:** `docs/DECISOES_PROJETO.md`

**Conteúdo:**
- Definição de risco de defasagem
- Categorização de IAN
- Escolha da base de dados
- Metodologia do modelo
- Justificativas técnicas

**Ações:**
- [ ] Documentar todas as decisões importantes
- [ ] Justificar escolhas técnicas
- [ ] Referenciar documentação PEDE

---

### **FASE 8: Preparação para Entrega** ⏱️ Prioridade ALTA

#### 8.1 Checklist Final
- [ ] Código no GitHub organizado
- [ ] Notebook de modelo preditivo completo
- [ ] Aplicação Streamlit funcionando
- [ ] Deploy realizado e testado
- [ ] README atualizado
- [ ] Documentação completa
- [ ] Testes realizados

#### 8.2 Organizar Repositório GitHub
**Estrutura Final:**
```
Datathon_F5/
├── app.py                          # Aplicação Streamlit
├── README.md                       # Documentação principal
├── requirements.txt                # Dependências
├── notebooks/
│   └── MODELO_PREDITIVO_DATATHON.ipynb
├── src/
│   ├── analise_exploratoria.py
│   └── modelagem.py
├── utils/
│   ├── database.py
│   ├── preprocessing.py
│   └── pede_calculations.py
├── database/
│   ├── schema.sql
│   └── migrate_excel_to_db.py
├── models/
│   └── modelo_risco_defasagem.pkl
├── docs/
│   ├── DEFINICOES_PEDE.md
│   └── DECISOES_PROJETO.md
└── output/
    ├── analise_exploratoria/
    └── modelagem/
```

---

## 📅 Cronograma Sugerido

### Semana 1: Migração e Correções
- **Dia 1-2:** Migração para base oficial Excel
- **Dia 3-4:** Validações e correções
- **Dia 5:** Re-treinar modelo

### Semana 2: Desenvolvimento Streamlit
- **Dia 1-2:** Estrutura básica da aplicação
- **Dia 3-4:** Funcionalidades de predição
- **Dia 5:** Dashboard e visualizações

### Semana 3: Finalização
- **Dia 1-2:** Deploy e testes
- **Dia 3:** Notebook de entrega
- **Dia 4:** Documentação final
- **Dia 5:** Revisão e ajustes finais

---

## ✅ Critérios de Sucesso

### Para Cada Fase:
1. ✅ Código funcionando
2. ✅ Testes realizados
3. ✅ Documentação atualizada
4. ✅ Compatibilidade mantida

### Para Entrega Final:
1. ✅ GitHub organizado e completo
2. ✅ Notebook demonstrando todas as etapas
3. ✅ Aplicação Streamlit funcionando
4. ✅ Deploy realizado e testado
5. ✅ Documentação clara e completa

---

## 🎯 Prioridades

### 🔴 ALTA (Fazer Primeiro):
1. Migração para base oficial Excel
2. Validações e correções
3. Aplicação Streamlit básica
4. Deploy

### 🟡 MÉDIA (Fazer Depois):
1. Re-treinar modelo
2. Notebook de entrega
3. Documentação adicional

### 🟢 BAIXA (Se sobrar tempo):
1. Melhorias de UI/UX
2. Visualizações adicionais
3. Otimizações

---

## 📝 Notas Importantes

1. **Preservar trabalho anterior:** Manter estrutura e código existente, apenas ajustar
2. **Usar base oficial:** Migrar para Excel oficial com INDE já calculado
3. **Documentar decisões:** Todas as escolhas técnicas devem estar documentadas
4. **Testar tudo:** Cada fase deve ser testada antes de avançar
5. **Manter coerência:** Alinhar com requisitos do Datathon

---

**Status:** 📋 Plano estruturado e pronto para execução

**Próximo passo:** Iniciar FASE 1 - Migração para Base Oficial
