# 📚 Alinhamento com Conceitos PEDE

## Situação Atual

O projeto utiliza os **indicadores PEDE** (IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE) que estão presentes nos dados, mas **não há verificação explícita** se as definições e interpretações estão alinhadas com o documento **"PEDE Pontos importantes.pdf"**.

---

## ✅ O que o Projeto Atualmente Faz

### Indicadores Utilizados:

1. **IAN** - Índice de Adequação de Nível
   - Categorização: severa (<5), moderada (5-7), em fase (>7)
   - Uso no modelo: Risco = IAN != 10

2. **IDA** - Índice de Desempenho Acadêmico
   - Análise de evolução por ano e fase
   - Correlação com outros indicadores

3. **IEG** - Índice de Engajamento Geral
   - Correlação com IDA e IPV
   - Feature importante no modelo

4. **IAA** - Índice de Autoavaliação
   - Correlação com IDA e IEG
   - Feature no modelo

5. **IPS** - Índice de Perfil Psicossocial
   - Correlação com IDA e IEG
   - Feature no modelo

6. **IPP** - Índice de Perfil Psicopedagógico
   - Correlação com IAN
   - Feature no modelo

7. **IPV** - Índice de Ponto de Virada
   - Análise de correlações
   - Feature no modelo

8. **INDE** - Índice Global
   - Consolidação por ano
   - Análise exploratória

---

## ⚠️ Pontos que Precisam de Verificação

### 1. **Definição de Risco de Defasagem**

**Atual no código:**
```python
df['Risco_defasagem'] = df['IAN'].apply(lambda x: 0 if x == 10 else 1)
```

**Questão:** Esta definição está alinhada com o conceito PEDE?

**Categorização IAN (usada na EDA):**
- Severa: IAN < 5
- Moderada: 5 <= IAN <= 7  
- Em fase: IAN > 7

**Possível Inconsistência:** 
- EDA categoriza de forma diferente
- Modelo usa IAN != 10 como risco
- Pode não estar alinhado com definição PEDE

### 2. **Escalas e Ranges**

Precisamos verificar se:
- Os indicadores estão na escala correta (0-10?)
- Os valores estão sendo interpretados corretamente
- As categorizações estão de acordo com PEDE

### 3. **Interpretação dos Indicadores**

Verificar se:
- Cada indicador está sendo usado conforme sua definição PEDE
- As relações entre indicadores fazem sentido conceitualmente
- As análises estão alinhadas com o propósito de cada indicador

---

## 📋 Checklist de Verificação

Para garantir alinhamento com PEDE, verificar:

- [ ] **Definições dos Indicadores**
  - [ ] IAN: Definição e interpretação corretas?
  - [ ] IDA: Reflete desempenho acadêmico conforme PEDE?
  - [ ] IEG: Captura engajamento conforme especificado?
  - [ ] IAA, IPS, IPP, IPV: Definições corretas?

- [ ] **Ranges e Escalas**
  - [ ] Indicadores na escala correta?
  - [ ] Categorizações (severa/moderada/em fase) corretas?
  - [ ] Valores sendo interpretados corretamente?

- [ ] **Definição de Risco**
  - [ ] Definição de risco alinhada com PEDE?
  - [ ] Categorias de defasagem corretas?

- [ ] **Relações entre Indicadores**
  - [ ] Correlações fazem sentido conceitualmente?
  - [ ] Modelo usa indicadores de forma coerente?

---

## 🔧 Ações Recomendadas

### 1. **Ler o PDF "PEDE Pontos importantes.pdf"**

Extrair:
- Definições exatas de cada indicador
- Escalas e ranges esperados
- Relações conceituais entre indicadores
- Definição correta de "risco de defasagem"
- Categorizações corretas

### 2. **Comparar com Implementação Atual**

Verificar:
- Se as definições no código estão corretas
- Se as escalas estão corretas
- Se a definição de risco está alinhada
- Se as categorizações estão corretas

### 3. **Ajustar se Necessário**

Se houver divergências:
- Corrigir definições no código
- Ajustar categorizações
- Atualizar documentação
- Re-treinar modelo se necessário

---

## 📝 Próximos Passos

1. **Você pode:**
   - Compartilhar o conteúdo do PDF (copiar texto ou descrever conceitos principais)
   - Ou me indicar quais conceitos específicos precisa verificar

2. **Eu posso:**
   - Analisar o conteúdo do PDF (se você compartilhar)
   - Comparar com a implementação atual
   - Identificar divergências
   - Propor correções

---

## 💡 Sugestão

**Opção 1:** Você compartilha os conceitos principais do PDF e eu verifico o alinhamento.

**Opção 2:** Você revisa o PDF e me indica quais conceitos específicos precisa verificar.

**Opção 3:** Criamos um documento de referência PEDE baseado no PDF para garantir alinhamento futuro.

---

**Status:** ⏳ Aguardando informações do PDF para verificação completa

**Ação Imediata:** Recomendo revisar o PDF e identificar se há divergências conceituais que precisam ser corrigidas.
