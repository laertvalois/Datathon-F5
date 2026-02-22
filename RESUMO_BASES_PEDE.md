# 📊 Resumo das Bases de Dados PEDE Disponíveis

## ✅ Base Oficial Principal

### **BASE DE DADOS PEDE 2024 - DATATHON.xlsx**

**Localização:** `Colab/Datathon/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`

**Estrutura:**
- **3 planilhas** (uma por ano):
  - `PEDE2022`: 860 registros
  - `PEDE2023`: 1.014 registros  
  - `PEDE2024`: 1.156 registros
  - **Total: 3.030 registros**

**Características:**
- ✅ **INDE já calculado** em cada planilha:
  - PEDE2022: `INDE 22`
  - PEDE2023: `INDE 23` e `INDE 2023`
  - PEDE2024: `INDE 2024` (e histórico `INDE 22`, `INDE 23`)

- ✅ **Todos os 7 indicadores presentes:**
  - IAN, IDA, IEG, IAA, IPS, IPP, IPV

- ✅ **Colunas principais:**
  - RA, Fase, Turma, Nome (anonimizado)
  - Idade, Gênero, Ano ingresso
  - Instituição de ensino
  - Notas: Mat, Por, Ing
  - Pedra (classificação por ano)
  - Defasagem, Fase Ideal
  - Destaques e recomendações

**Vantagens:**
- ✅ Base oficial e atualizada
- ✅ INDE já calculado (não precisa recalcular)
- ✅ Estrutura consistente entre anos
- ✅ Dados mais completos e organizados

**Diferenças entre anos:**
- 2022: 42 colunas, sem IPP
- 2023: 48 colunas, com IPP
- 2024: 50 colunas, mais campos de status

---

## 📁 Outras Bases Disponíveis

### 1. **PEDE_PASSOS_DATASET_FIAP.csv/xlsx**

**Localização:** `Colab/Datathon/Bases antigas/PEDE_PASSOS_DATASET_FIAP.csv`

**Características:**
- 1.349 registros
- 69 colunas
- Dados de 2020, 2021 e 2022
- Separador: `;` (ponto e vírgula)
- Estrutura longitudinal (múltiplos anos por aluno)

**Uso:** Pode ser útil para análises históricas ou comparações temporais

---

### 2. **Base de Dados - Passos Mágicos** (Estrutura Relacional)

**Localização:** `Colab/Datathon/Bases antigas/Base de dados - Passos Mágicos/`

**Estrutura:**
Múltiplas tabelas relacionais:

- **TbAluno** - Dados dos alunos
- **TbFase** - Dados das fases
- **TbTurma** - Dados das turmas
- **TbDiario** - Diários de aula
- **TbHistorico** - Histórico de notas
- **TbMeta** - Metas dos alunos
- **TbProfessor** - Dados dos professores
- **TbResponsavel** - Responsáveis
- **Outras tabelas** - Centro de resultado, cursos, disciplinas, etc.

**Uso:** Para análises mais profundas com relacionamentos entre entidades

---

## 📚 Documentos de Referência

### PDFs Disponíveis:

1. **Relatório PEDE2020.pdf** ✅
   - Definições dos indicadores
   - Ponderações do INDE
   - Conceitos fundamentais

2. **Relatório PEDE2021.pdf**
   - Relatório do ano 2021

3. **Relatorio PEDE2022.pdf**
   - Relatório do ano 2022

4. **Dicionário Dados Datathon.pdf** ✅
   - Dicionário de dados
   - Definições de campos

5. **desvendando_passos.pdf**
   - Informações sobre a Passos Mágicos

### DOCX Disponíveis:

1. **PEDE_ Pontos importantes.docx** ✅
   - Pontos importantes sobre o PEDE

2. **Links adicionais da passos.docx**
   - Links e referências adicionais

---

## 🎯 Recomendações de Uso

### Para o Projeto Atual:

#### ✅ **USAR: BASE DE DADOS PEDE 2024 - DATATHON.xlsx**

**Motivos:**
1. ✅ **Base oficial** - Mais confiável
2. ✅ **INDE já calculado** - Não precisa recalcular
3. ✅ **Dados atualizados** - 2022, 2023, 2024
4. ✅ **Estrutura completa** - Todos os indicadores
5. ✅ **Consistência** - Estrutura similar entre anos

**Ação Recomendada:**
- Substituir os CSVs atuais por esta base Excel
- Criar script de migração específico para este formato
- Usar INDE já calculado (não recalcular)

---

### Para Análises Adicionais:

#### 1. **PEDE_PASSOS_DATASET_FIAP.csv**
- Útil para análises longitudinais (2020-2022)
- Comparações temporais mais longas

#### 2. **Base Relacional (TbAluno, TbFase, etc.)**
- Para análises mais profundas
- Relacionamentos entre entidades
- Análises de frequência, histórico, etc.

#### 3. **Documentos PDF/DOCX**
- Referência para definições
- Validação de conceitos
- Documentação do projeto

---

## 🔧 Próximos Passos Sugeridos

### 1. Migrar para Base Oficial Excel

**Criar script:** `database/migrate_excel_to_db.py`

**Vantagens:**
- Usar INDE já calculado (oficial)
- Dados mais completos
- Estrutura mais consistente

### 2. Atualizar Estrutura do Banco

**Ajustes necessários:**
- Adicionar campos novos (Pedra, Destaques, etc.)
- Manter compatibilidade com código existente
- Incluir histórico de INDE (INDE 22, INDE 23, INDE 2024)

### 3. Validar Dados

**Verificações:**
- Comparar INDE da base oficial com cálculos PEDE
- Validar consistência entre anos
- Verificar completude dos dados

---

## 📋 Comparação: Base Atual vs Base Oficial

| Aspecto | Base Atual (CSVs) | Base Oficial (Excel) |
|---------|-------------------|---------------------|
| **Fonte** | GitHub (pode estar desatualizada) | Oficial Passos Mágicos |
| **INDE** | Pode ter divergências | ✅ Já calculado oficialmente |
| **Anos** | 2022, 2023, 2024 | 2022, 2023, 2024 |
| **Registros** | ~3.000 | 3.030 (oficial) |
| **Estrutura** | Similar | Mais completa |
| **Campos extras** | Limitados | Pedra, Destaques, Recomendações |

---

## ✅ Conclusão

**A base oficial Excel (`BASE DE DADOS PEDE 2024 - DATATHON.xlsx`) é a melhor opção porque:**

1. ✅ É a base oficial da Passos Mágicos
2. ✅ INDE já está calculado corretamente
3. ✅ Dados mais completos e atualizados
4. ✅ Estrutura consistente entre anos
5. ✅ Campos adicionais úteis (Pedra, Destaques, etc.)

**Recomendação:** Migrar para esta base oficial e usar o INDE já calculado.

---

**Status:** ✅ Bases identificadas e analisadas

**Próxima ação:** Criar script de migração para base oficial Excel
