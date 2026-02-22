# 📚 Verificação de Alinhamento com Conceitos PEDE

## Objetivo

Verificar se o projeto está utilizando corretamente os conceitos e definições do arquivo **"PEDE Pontos importantes.pdf"**.

---

## 📋 Indicadores PEDE Utilizados no Projeto

### Indicadores Identificados no Código:

1. **IAN** - Índice de Adequação de Nível
2. **IDA** - Índice de Desempenho Acadêmico
3. **IEG** - Índice de Engajamento Geral
4. **IAA** - Índice de Autoavaliação
5. **IPS** - Índice de Perfil Psicossocial
6. **IPP** - Índice de Perfil Psicopedagógico
7. **IPV** - Índice de Ponto de Virada
8. **INDE** - Índice Global

---

## 🔍 Verificações Necessárias

Para garantir que o projeto está alinhado com os conceitos do PEDE, precisamos verificar:

### 1. **Definições dos Indicadores**
- [ ] IAN está sendo calculado/interpretado corretamente?
- [ ] IDA reflete o desempenho acadêmico conforme definição PEDE?
- [ ] IEG captura o engajamento conforme especificado?
- [ ] IAA, IPS, IPP, IPV estão sendo usados conforme suas definições?

### 2. **Ranges e Escalas**
- [ ] Os indicadores estão na escala correta (0-10, 0-100, etc.)?
- [ ] As categorizações (ex: IAN severa/moderada/em fase) estão corretas?
- [ ] Os valores estão sendo interpretados corretamente?

### 3. **Relações entre Indicadores**
- [ ] As correlações analisadas fazem sentido do ponto de vista conceitual?
- [ ] O modelo preditivo usa os indicadores de forma coerente?

### 4. **Definição de Risco de Defasagem**
- [ ] A definição de risco (IAN != 10) está alinhada com o conceito PEDE?
- [ ] As categorias de defasagem (severa, moderada, em fase) estão corretas?

---

## ⚠️ Pontos de Atenção Identificados

### 1. **Definição de Risco no Modelo**

**Atual:**
```python
df['Risco_defasagem'] = df['IAN'].apply(lambda x: 0 if x == 10 else 1)
```

**Questão:** Esta definição está alinhada com o conceito PEDE de defasagem?

**Categorização IAN (EDA):**
- Severa: IAN < 5
- Moderada: 5 <= IAN <= 7
- Em fase: IAN > 7

**Possível Inconsistência:** O modelo considera "em risco" qualquer IAN != 10, mas a EDA categoriza de forma diferente.

### 2. **Interpretação dos Indicadores**

Precisamos verificar se:
- Os indicadores estão sendo interpretados conforme suas definições no PEDE
- As escalas estão corretas
- As relações entre indicadores fazem sentido conceitualmente

---

## 📝 Próximos Passos

1. **Ler o arquivo PDF** "PEDE Pontos importantes.pdf" para entender:
   - Definições exatas de cada indicador
   - Escalas e ranges esperados
   - Relações conceituais entre indicadores
   - Definição correta de "risco de defasagem"

2. **Comparar com implementação atual:**
   - Verificar se as definições estão corretas
   - Ajustar se necessário

3. **Documentar:**
   - Criar documento com definições PEDE
   - Garantir que código e documentação estejam alinhados

---

## 🔧 Ações Recomendadas

### Se houver divergências:

1. **Ajustar definições no código:**
   - Corrigir cálculo/interpretação de indicadores
   - Ajustar definição de risco se necessário

2. **Atualizar documentação:**
   - Incluir referências ao PEDE
   - Documentar definições utilizadas

3. **Validar com especialistas:**
   - Confirmar interpretações com equipe PEDE/Passos Mágicos

---

## 📄 Nota

**Este documento é um template de verificação.** 

Para completar a verificação, é necessário:
1. Ler o arquivo "PEDE Pontos importantes.pdf"
2. Comparar com as implementações atuais
3. Identificar e corrigir divergências

---

**Status:** ⏳ Aguardando leitura do PDF para verificação completa
