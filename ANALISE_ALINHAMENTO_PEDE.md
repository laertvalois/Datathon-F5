# 📚 Análise de Alinhamento com PEDE 2020

## 📋 Definições dos Indicadores (Conforme PEDE 2020)

### Estrutura do INDE

O **INDE (Índice de Desenvolvimento Educacional)** é formado por 7 indicadores com ponderações diferentes:

**Para Fases 0 a 7:**
```
INDE = IAN x 0.1 + IDA x 0.2 + IEG x 0.2 + IAA x 0.1 + IPS x 0.1 + IPP x 0.1 + IPV x 0.2
```

**Para Fase 8:**
```
INDE = IAN x 0.1 + IDA x 0.4 + IEG x 0.2 + IAA x 0.1 + IPS x 0.2
```
*(Sem IPP e IPV para Fase 8)*

---

### Definições dos Indicadores

#### 1. **IAN - Indicador de Adequação de Nível**
- **Definição PEDE:** Registra a defasagem da aprendizagem do aluno por meio da comparação da Fase atual do aluno na Associação com a equivalência das Fases de ensino da Associação e a divisão dos anos escolares do ensino formal (por idade).
- **Escala:** 0 a 10 pontos
- **Peso no INDE:** 10% (Fases 0-7 e Fase 8)
- **Fonte:** Registros administrativos

#### 2. **IDA - Indicador de Desempenho Acadêmico**
- **Definição PEDE:** 
  - **Fases 0-7:** Proficiência do aluno nos exames padronizados de avaliação interna das disciplinas oferecidas pela Associação
  - **Fase 8:** Nota média obtida pelos alunos em todas as disciplinas curriculares cursadas nas instituições de ensino superior
- **Escala:** 0 a 10 pontos
- **Peso no INDE:** 20% (Fases 0-7), 40% (Fase 8)
- **Fonte:** Notas Provas PM e Média Geral Universitária

#### 3. **IEG - Indicador de Engajamento**
- **Definição PEDE:**
  - **Fases 0-7:** Mede o engajamento do aluno nas tarefas curriculares (lição de casa)
  - **Fase 8:** Engajamento em ações de voluntariado
- **Escala:** 0 a 10 pontos (transposição do percentual de entregas)
- **Peso no INDE:** 20% (ambas as faixas)
- **Fonte:** Registros de entrega de lição de casa e de voluntariado

#### 4. **IAA - Indicador de Autoavaliação**
- **Definição PEDE:** Registra por meio de um questionário padronizado e adaptado às distintas faixas etárias, uma autoavaliação do aluno sobre como se sente consigo mesmo, sobre os estudos, sobre sua família, amigos e comunidade, e sobre como se sente a respeito da Associação Passos Mágicos.
- **Escala:** 0 a 10 pontos
- **Peso no INDE:** 10% (ambas as faixas)
- **Fonte:** Questionário de Autoavaliação individual

#### 5. **IPS - Indicador Psicossocial**
- **Definição PEDE:** Avaliação da equipe de psicólogas para caracterizar o desenvolvimento do aluno nas suas interações familiares, no seu desenvolvimento emocional, comportamental e da sua socialização na vida comunitária. Também caracteriza o tipo de atendimento psicológico oferecido.
- **Escala:** 0 a 10 pontos
- **Peso no INDE:** 10% (Fases 0-7), 20% (Fase 8)
- **Fonte:** Questionário individual de avaliação das psicólogas

#### 6. **IPP - Indicador Psicopedagógico**
- **Definição PEDE:** Avaliação da equipe de educadores e psicopedagogos para caracterizar o desenvolvimento cognitivo, emocional, comportamental e de socialização do aluno no seu processo de aprendizado dentro do Programa de Aceleração do Conhecimento.
- **Escala:** 0 a 10 pontos (questionário padronizado de 4 perguntas)
- **Peso no INDE:** 10% (Fases 0-7), N/A (Fase 8)
- **Fonte:** Questionário individual de avaliação dos pedagogos e professores

#### 7. **IPV - Indicador do Ponto de Virada**
- **Definição PEDE:** Avaliação da equipe de educadores e psicopedagogos sobre o desenvolvimento do aluno das aptidões necessárias para iniciar a transformação da sua vida por meio da Educação, avaliando a integração do aluno à Associação, o seu desenvolvimento emocional, e o seu potencial acadêmico.
- **Escala:** 0 a 10 pontos (questionário padronizado de 9 perguntas ponderadas)
- **Peso no INDE:** 20% (Fases 0-7), N/A (Fase 8)
- **Fonte:** Questionário individual de avaliação dos pedagogos e professores

---

## ⚠️ Análise de Alinhamento com o Projeto Atual

### ✅ **Pontos Alinhados:**

1. **Escalas dos Indicadores:**
   - ✅ Todos os indicadores estão na escala 0 a 10 pontos (conforme PEDE)
   - ✅ O projeto usa essa escala corretamente

2. **Uso dos Indicadores:**
   - ✅ Todos os 7 indicadores estão sendo utilizados no projeto
   - ✅ Indicadores estão sendo analisados e usados no modelo

3. **Estrutura Geral:**
   - ✅ Projeto reconhece as dimensões (Acadêmica, Psicossocial, Psicopedagógica)
   - ✅ Análises de correlação fazem sentido conceitualmente

---

### ❌ **Divergências Identificadas:**

#### 1. **Definição de Risco de Defasagem - CRÍTICO**

**Código Atual:**
```python
df['Risco_defasagem'] = df['IAN'].apply(lambda x: 0 if x == 10 else 1)
```

**Problema:**
- O código assume que `IAN == 10` significa "sem risco"
- Mas o IAN mede **adequação de nível** (comparação idade/Fase)
- **IAN = 10** pode significar que o aluno está na fase adequada para sua idade
- **IAN < 10** indica defasagem (aluno em fase anterior à adequada para sua idade)

**Análise:**
- A definição atual pode estar **parcialmente correta**, mas precisa de validação:
  - Se IAN = 10 significa "adequado" → sem risco ✅
  - Se IAN < 10 significa "defasado" → em risco ✅
  - Mas a categorização usada na EDA (severa <5, moderada 5-7, em fase >7) sugere que IAN > 7 já é considerado "em fase"

**Questão:** Qual é a interpretação correta do IAN?
- IAN = 10: Aluno na fase adequada para idade?
- IAN < 10: Quanto menor, maior a defasagem?
- IAN > 10: É possível? (pode indicar aluno avançado?)

#### 2. **Categorização de IAN**

**Código Atual:**
```python
# Severa: IAN < 5
# Moderada: 5 <= IAN <= 7
# Em fase: IAN > 7
```

**Problema:**
- Essa categorização **não está explicitada no documento PEDE 2020**
- O documento não define categorias de defasagem baseadas em ranges do IAN
- Pode ser uma interpretação do time, mas precisa ser validada

**Recomendação:** Verificar se essa categorização está em outro documento ou se foi definida pela equipe.

#### 3. **Cálculo do INDE**

**Problema:**
- O projeto **não calcula o INDE** usando as ponderações corretas do PEDE
- O código apenas consolida INDE_22, INDE_23, INDE_24 (valores já calculados)
- Não há verificação se o INDE foi calculado corretamente

**Ponderações Corretas (Fases 0-7):**
```
INDE = IAN x 0.1 + IDA x 0.2 + IEG x 0.2 + IAA x 0.1 + IPS x 0.1 + IPP x 0.1 + IPV x 0.2
```

**Ação Necessária:** Verificar se o INDE nos dados foi calculado corretamente ou recalcular se necessário.

#### 4. **Tratamento de Fase 8**

**Problema:**
- O projeto não diferencia Fase 8 das demais fases
- Fase 8 tem:
  - Composição diferente do INDE (sem IPP e IPV)
  - Ponderações diferentes (IDA = 40% ao invés de 20%)
  - IDA calculado diferente (média universitária)

**Ação Necessária:** Implementar lógica diferenciada para Fase 8.

---

## 🔧 Correções Necessárias

### Prioridade ALTA:

1. **Validar Definição de Risco:**
   - Confirmar interpretação do IAN
   - Ajustar definição de risco se necessário
   - Documentar justificativa

2. **Validar Categorização de IAN:**
   - Verificar se categorias (severa/moderada/em fase) estão corretas
   - Documentar origem das categorias

3. **Verificar Cálculo do INDE:**
   - Validar se INDE nos dados foi calculado corretamente
   - Implementar função de cálculo do INDE com ponderações corretas

### Prioridade MÉDIA:

4. **Tratamento de Fase 8:**
   - Implementar lógica diferenciada para Fase 8
   - Ajustar cálculos e análises

5. **Documentação:**
   - Documentar definições dos indicadores conforme PEDE
   - Incluir referências ao documento PEDE 2020

---

## 📝 Recomendações Imediatas

### 1. Criar Função de Validação do INDE

```python
def calcular_inde_pede(df, fase_col='Fase'):
    """
    Calcula INDE conforme ponderações do PEDE 2020.
    """
    df = df.copy()
    
    # Fases 0-7
    mask_fases_0_7 = df[fase_col].isin([0, 1, 2, 3, 4, 5, 6, 7, 'ALFA'])
    df.loc[mask_fases_0_7, 'INDE_calculado'] = (
        df.loc[mask_fases_0_7, 'IAN'] * 0.1 +
        df.loc[mask_fases_0_7, 'IDA'] * 0.2 +
        df.loc[mask_fases_0_7, 'IEG'] * 0.2 +
        df.loc[mask_fases_0_7, 'IAA'] * 0.1 +
        df.loc[mask_fases_0_7, 'IPS'] * 0.1 +
        df.loc[mask_fases_0_7, 'IPP'] * 0.1 +
        df.loc[mask_fases_0_7, 'IPV'] * 0.2
    )
    
    # Fase 8
    mask_fase_8 = df[fase_col] == 8
    df.loc[mask_fase_8, 'INDE_calculado'] = (
        df.loc[mask_fase_8, 'IAN'] * 0.1 +
        df.loc[mask_fase_8, 'IDA'] * 0.4 +
        df.loc[mask_fase_8, 'IEG'] * 0.2 +
        df.loc[mask_fase_8, 'IAA'] * 0.1 +
        df.loc[mask_fase_8, 'IPS'] * 0.2
    )
    
    return df
```

### 2. Documentar Definições

Criar arquivo `docs/DEFINICOES_PEDE.md` com todas as definições.

### 3. Validar Definição de Risco

Consultar especialistas ou documentação adicional sobre interpretação do IAN.

---

## ✅ Conclusão

O projeto está **parcialmente alinhado** com os conceitos PEDE:

- ✅ **Alinhado:** Escalas, uso dos indicadores, estrutura geral
- ⚠️ **Precisa Validação:** Definição de risco, categorização de IAN
- ❌ **Divergências:** Cálculo do INDE, tratamento de Fase 8

**Próximo Passo:** Implementar correções prioritárias e validar definições.
