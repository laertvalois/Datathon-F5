# 🚀 Guia de Deploy - Streamlit Community Cloud

Este guia explica como fazer o deploy da aplicação Streamlit no Streamlit Community Cloud.

---

## 📋 Pré-requisitos

### 1. Arquivos Necessários no Repositório

Certifique-se de que os seguintes arquivos estão no repositório GitHub:

```
Datathon_F5/
├── app.py                          ✅ Arquivo principal do Streamlit
├── requirements.txt                ✅ Dependências Python
├── .streamlit/
│   └── config.toml                 ✅ Configurações do Streamlit
├── models/
│   └── modelo_risco_defasagem.pkl  ✅ Modelo treinado
├── data/
│   └── datathon_f5.db              ✅ Banco de dados SQLite
├── src/                            ✅ Módulos de análise
├── utils/                          ✅ Utilitários
└── database/                       ✅ Scripts de migração
```

### 2. Verificar `.gitignore`

O arquivo `.gitignore` deve permitir:
- ✅ `data/datathon_f5.db` (banco de dados)
- ✅ `models/modelo_risco_defasagem.pkl` (modelo treinado)

---

## 🔧 Passo a Passo do Deploy

### 1. Preparar Repositório GitHub

```bash
# Verificar status
git status

# Adicionar arquivos necessários
git add app.py
git add requirements.txt
git add .streamlit/
git add models/modelo_risco_defasagem.pkl
git add data/datathon_f5.db
git add src/ utils/ database/

# Commit
git commit -m "Preparar para deploy no Streamlit Cloud"

# Push
git push origin main
```

### 2. Acessar Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**

### 3. Configurar Aplicação

**Configurações:**

- **Repository:** Selecione o repositório `Datathon_F5`
- **Branch:** `main` (ou a branch desejada)
- **Main file path:** `app.py`
- **App URL:** (opcional) Personalize a URL

**Avançado (opcional):**

- **Python version:** Deixe o padrão (3.8+)
- **Secrets:** Não necessário para este projeto

### 4. Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (pode levar 2-5 minutos)
3. A aplicação estará disponível em: `https://[seu-app].streamlit.app`

---

## ✅ Verificação Pós-Deploy

### Checklist de Testes

Após o deploy, teste:

- [ ] **Página Início** carrega corretamente
- [ ] **Predição Individual** funciona
- [ ] **Modelo Preditivo** exibe visualizações (ROC e Confusão)
- [ ] **Indicadores** carregam dados e gráficos
- [ ] **Sobre o Sistema** exibe informações corretas

### Possíveis Problemas

#### 1. Erro: "Banco de dados não encontrado"

**Solução:**
- Verifique se `data/datathon_f5.db` está no repositório
- Verifique se `.gitignore` não está ignorando o arquivo

#### 2. Erro: "Modelo não encontrado"

**Solução:**
- Verifique se `models/modelo_risco_defasagem.pkl` está no repositório
- Verifique se `.gitignore` não está ignorando o arquivo

#### 3. Erro de Importação

**Solução:**
- Verifique se `requirements.txt` está completo
- Verifique se todos os módulos (`src/`, `utils/`) estão no repositório

#### 4. App lento

**Solução:**
- O app usa cache do Streamlit (`@st.cache_data`, `@st.cache_resource`)
- Primeira carga pode ser mais lenta
- Verifique se o banco de dados não está muito grande

---

## 📊 Monitoramento

### Logs

Acesse os logs do app em:
- Streamlit Cloud Dashboard → Seu App → Logs

### Métricas

Monitore:
- Tempo de resposta
- Uso de memória
- Erros no console

---

## 🔄 Atualizações

Para atualizar o app:

1. Faça alterações no código
2. Commit e push para GitHub
3. O Streamlit Cloud detecta automaticamente e faz redeploy
4. Aguarde alguns minutos para o novo deploy

---

## 📝 Notas Importantes

1. **Banco de Dados:**
   - O arquivo `data/datathon_f5.db` (~1.3MB) está incluído no repositório
   - Se precisar atualizar, execute `python database/migrate_excel_to_db.py` localmente e faça commit

2. **Modelo:**
   - O arquivo `models/modelo_risco_defasagem.pkl` (~1MB) está incluído no repositório
   - Para retreinar, execute `python scripts/run_modelagem.py` localmente e faça commit

3. **Performance:**
   - O app usa cache extensivamente para melhor performance
   - Primeira carga pode ser mais lenta

4. **Limites do Streamlit Cloud:**
   - Apps gratuitos têm limites de uso
   - Se o app ficar inativo, pode demorar para iniciar

---

## 🎯 Próximos Passos Após Deploy

1. ✅ Testar todas as funcionalidades
2. ✅ Compartilhar link do app
3. ✅ Atualizar README.md com link do deploy
4. ✅ Documentar no repositório GitHub

---

**Status:** ✅ Pronto para deploy

**Última atualização:** Após implementação das visualizações dinâmicas
