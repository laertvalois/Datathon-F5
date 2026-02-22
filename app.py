"""
Aplicação Streamlit - Análise Completa Datathon F5
Passos Mágicos - Respondendo às 11 Perguntas do Datathon
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, accuracy_score, roc_curve, confusion_matrix
from sklearn.model_selection import train_test_split

from utils.database import get_db_manager
from utils.preprocessing import preprocess_for_eda, preprocess_for_modeling, create_nivel_ian

# Configuração da página
st.set_page_config(
    page_title="Passos Mágicos - Análise Completa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Minimalista inspirado no Solarin, usando cores padrão do Streamlit
st.markdown("""
    <style>
    /* Importa fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Base - Usa cores padrão do Streamlit */
    html, body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header principal - Minimalista e elegante */
    .main-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 0.01em;
        text-transform: uppercase;
        opacity: 0.8;
    }
    
    /* Question header - Clean com borda sutil */
    .question-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.75rem;
        font-weight: 600;
        margin-top: 3rem;
        margin-bottom: 2rem;
        padding: 1.5rem 0;
        border-bottom: 2px solid;
        letter-spacing: -0.01em;
    }
    
    /* Insight boxes - Minimalista com fundo sutil */
    .insight-box {
        background-color: rgba(0, 0, 0, 0.03);
        padding: 1.5rem;
        border-radius: 0;
        border-left: 3px solid;
        margin: 1.5rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Botões - Clean e minimalista */
    .stButton>button {
        width: 100%;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        border-radius: 0;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.875rem;
    }
    
    /* Métricas - Clean design */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        opacity: 0.7;
    }
    
    /* Sidebar - Minimalista */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Títulos de seção */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    
    h1 {
        font-size: 2.5rem;
    }
    
    h2 {
        font-size: 2rem;
    }
    
    h3 {
        font-size: 1.5rem;
    }
    
    /* Tabelas - Clean */
    table {
        border-collapse: collapse;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    th {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        padding: 1rem;
    }
    
    td {
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        padding: 0.75rem 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Inputs - Minimalista */
    .stNumberInput>div>div>input,
    .stSlider>div>div>div>div {
        border-radius: 0;
    }
    
    /* Selectbox e multiselect */
    .stSelectbox>div>div,
    .stMultiSelect>div>div {
        border-radius: 0;
    }
    
    /* Cards de métricas */
    [data-testid="stMetricContainer"] {
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        border-radius: 0;
    }
    
    /* Alerts - Minimalista */
    .stAlert {
        border-radius: 0;
        border-left: 3px solid;
        font-family: 'Inter', sans-serif;
    }
    
    /* Gráficos - Espaçamento */
    .js-plotly-plot {
        margin: 2rem 0;
    }
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 0, 0, 0.5);
    }
    
    /* Links */
    a {
        text-decoration: underline;
        text-decoration-thickness: 1px;
        text-underline-offset: 2px;
    }
    
    a:hover {
        text-decoration-thickness: 2px;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        margin: 3rem 0;
    }
    
    /* Markdown text */
    .stMarkdown {
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
    }
    
    .stMarkdown strong {
        font-weight: 600;
    }
    
    /* Code blocks */
    code {
        background-color: rgba(0, 0, 0, 0.05);
        padding: 0.2rem 0.4rem;
        border-radius: 0;
        font-family: 'Courier New', monospace;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Remove padding extra do Streamlit */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Radio buttons - Clean */
    .stRadio>div {
        gap: 1rem;
    }
    
    .stRadio>div>label {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Carrega o modelo treinado."""
    # Usa caminho absoluto baseado no diretório do app.py
    base_dir = Path(__file__).parent
    model_path = base_dir / 'models' / 'modelo_risco_defasagem.pkl'
    
    # Tenta caminho alternativo se não encontrar
    if not model_path.exists():
        # Tenta caminho relativo também
        alt_path = Path('models/modelo_risco_defasagem.pkl')
        if alt_path.exists():
            model_path = alt_path
        else:
            st.error(f"Modelo não encontrado. Procurou em: {model_path} e {alt_path}")
            st.info("Verifique se o arquivo 'models/modelo_risco_defasagem.pkl' está no repositório.")
            return None
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error(f"Arquivo do modelo não encontrado: {model_path}")
        return None
    except pickle.UnpicklingError as e:
        st.error(f"Erro ao deserializar modelo (arquivo pode estar corrompido): {e}")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {type(e).__name__}: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None


@st.cache_data
def load_data():
    """Carrega dados do banco."""
    try:
        db = get_db_manager()
        df = db.load_data_for_eda()
        df = preprocess_for_eda(df)
        # Garante que Nivel_IAN existe
        if 'Nivel_IAN' not in df.columns:
            df['Nivel_IAN'] = create_nivel_ian(df)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None


@st.cache_data
def load_data_for_modeling():
    """Carrega dados formatados para modelagem."""
    try:
        db = get_db_manager()
        df = db.load_data_for_modeling()
        df = preprocess_for_modeling(df)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados para modelagem: {e}")
        return None


def generate_roc_curve(model, X_test, y_test):
    """Gera curva ROC usando Plotly."""
    try:
        # Calcula probabilidades
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calcula curva ROC
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # Cria gráfico Plotly
        fig = go.Figure()
        
        # Curva ROC
        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name=f'ROC Curve (AUC = {auc_score:.3f})',
            line=dict(width=3, color='#1f77b4')
        ))
        
        # Linha diagonal (classificador aleatório)
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(width=2, color='red', dash='dash')
        ))
        
        fig.update_layout(
            title='Curva ROC - Hist Gradient Boosting',
            xaxis_title='Taxa de Falsos Positivos (FPR)',
            yaxis_title='Taxa de Verdadeiros Positivos (TPR)',
            width=800,
            height=600,
            hovermode='x unified',
            legend=dict(x=0.6, y=0.1)
        )
        
        return fig, auc_score
    except Exception as e:
        st.error(f"Erro ao gerar curva ROC: {e}")
        return None, None


def generate_confusion_matrix_plot(model, X_test, y_test):
    """Gera matriz de confusão usando Plotly."""
    try:
        # Calcula predições
        y_pred = model.predict(X_test)
        
        # Calcula matriz de confusão
        cm = confusion_matrix(y_test, y_pred)
        
        # Labels
        labels = ['Sem Risco', 'Em Risco']
        
        # Cria heatmap com Plotly
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale='Blues',
            text=cm,
            texttemplate='%{text}',
            textfont={"size": 16},
            hoverongaps=False
        ))
        
        # Adiciona anotações com percentuais
        annotations = []
        total = cm.sum()
        for i in range(len(labels)):
            for j in range(len(labels)):
                value = cm[i][j]
                pct = (value / total * 100) if total > 0 else 0
                annotations.append(
                    dict(
                        x=j,
                        y=i,
                        text=f'{value}<br>({pct:.1f}%)',
                        showarrow=False,
                        font=dict(color='white' if cm[i][j] > cm.max() / 2 else 'black', size=14)
                    )
                )
        
        fig.update_layout(
            title='Matriz de Confusão - Hist Gradient Boosting',
            xaxis_title='Predito',
            yaxis_title='Real',
            width=600,
            height=600,
            annotations=annotations
        )
        
        # Calcula métricas
        tn, fp, fn, tp = cm.ravel()
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'tn': tn,
            'fp': fp,
            'fn': fn,
            'tp': tp
        }
        
        return fig, metrics
    except Exception as e:
        st.error(f"Erro ao gerar matriz de confusão: {e}")
        return None, None


def main():
    """Função principal da aplicação."""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Passos Mágicos</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Análise Completa de Risco de Defasagem Educacional</p>', unsafe_allow_html=True)
    
    # Sidebar - Menu principal
    st.sidebar.markdown("## 🎓 Passos Mágicos")
    st.sidebar.markdown("---")
    
    # Menu principal como lista (radio buttons)
    menu_selecionado = st.sidebar.radio(
        "Navegação",
        [
            "🏠 Início",
            "🔮 Predição Individual de Risco",
            "🤖 Modelo Preditivo",
            "📊 Indicadores",
            "ℹ️ Sobre o Sistema"
        ],
        label_visibility="collapsed"
    )
    
    # Se Indicadores foi selecionado, mostra submenu
    if menu_selecionado == "📊 Indicadores":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Indicadores PEDE")
        
        indicador_selecionado = st.sidebar.radio(
            "Selecione:",
            [
                "IAN - Adequação do Nível",
                "IDA - Desempenho Acadêmico",
                "IEG - Engajamento",
                "IAA - Autoavaliação",
                "IPS - Psicossocial",
                "IPP - Psicopedagógico",
                "IPV - Ponto de Virada",
                "INDE - Multidimensionalidade"
            ],
            label_visibility="collapsed"
        )
        
        # Extrai o nome do indicador
        indicador_nome = indicador_selecionado.split(" - ", 1)[1] if " - " in indicador_selecionado else indicador_selecionado
    else:
        indicador_nome = None
    
    # Carrega dados uma vez
    df = load_data()
    
    # Roteamento principal
    if menu_selecionado == "🏠 Início":
        show_inicio_completo(df)
    
    elif menu_selecionado == "🔮 Predição Individual de Risco":
        show_prediction()
    
    elif menu_selecionado == "🤖 Modelo Preditivo":
        show_modelo_preditivo_completo(df)
    
    elif menu_selecionado == "📊 Indicadores":
        show_indicadores(df, indicador_nome)
    
    elif menu_selecionado == "ℹ️ Sobre o Sistema":
        show_sobre_sistema()


def show_inicio_completo(df):
    """Página Início completa com todas as seções."""
    
    # Usa abas para organizar o conteúdo
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Objetivo",
        "🔮 Predição",
        "📊 Insights e Métricas",
        "🔧 Informações Técnicas",
        "📚 Recursos",
        "📖 Como Usar"
    ])
    
    with tab1:
        st.markdown("## 🎯 Objetivo")
        
        st.markdown("""
        ### Sobre a Passos Mágicos
        
        A Associação Passos Mágicos tem uma trajetória de 32 anos de atuação, trabalhando na 
        transformação da vida de crianças e jovens de baixa renda, os levando a melhores 
        oportunidades de vida.
        
        ### Objetivo do Sistema
        
        Este sistema foi desenvolvido para o **Datathon F5** com o objetivo de:
        
        - **Identificar proativamente** alunos em risco de defasagem educacional
        - **Fornecer insights** baseados em dados para tomada de decisão
        - **Apoiar intervenções** pedagógicas e psicopedagógicas personalizadas
        - **Monitorar a evolução** dos indicadores educacionais ao longo do tempo
        
        ### Metodologia
        
        Utilizamos técnicas de **Data Analytics** e **Machine Learning** para:
        
        1. Analisar indicadores educacionais (IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE)
        2. Identificar padrões de risco de defasagem
        3. Construir modelo preditivo para antecipar alunos em risco
        4. Disponibilizar solução via aplicação web interativa
        
        ### Impacto Esperado
        
        Com este sistema, a Passos Mágicos pode:
        
        - Intervir **antes** que a defasagem se agrave
        - Alocar recursos de forma mais eficiente
        - Personalizar estratégias de apoio por aluno
        - Monitorar a efetividade do programa
        """)
    
    with tab2:
        st.markdown("## 🔮 Predição")
        
        st.markdown("""
        ### Sistema de Predição de Risco
        
        O sistema utiliza um modelo de **Machine Learning** (Hist Gradient Boosting) 
        treinado com dados históricos da Passos Mágicos para prever o risco de defasagem 
        educacional.
        
        ### Como Funciona
        
        1. **Coleta de Dados:** O sistema analisa 14 features do aluno:
           - Dados demográficos (Idade, Ano de ingresso)
           - Indicadores PEDE (IAA, IEG, IPS, IPP, IDA, IPV)
           - Notas acadêmicas (Matemática, Português, Inglês)
           - Features derivadas (Tempo na escola, Médias)
        
        2. **Processamento:** Os dados são pré-processados e normalizados
        
        3. **Predição:** O modelo calcula a probabilidade de risco
        
        4. **Resultado:** Classificação em "Em Risco" ou "Sem Risco" com probabilidade
        
        ### Performance do Modelo
        
        - **Acurácia:** ~92%
        - **ROC-AUC:** ~96%
        - **F1-Score:** ~92%
        
        ### Acesse
        
        Use o menu lateral para acessar **"Predição Individual de Risco"** e fazer 
        predições para alunos específicos.
        """)
    
    with tab3:
        st.markdown("## 📊 Insights e Métricas")
        
        if df is None:
            st.error("Erro ao carregar dados.")
        else:
            st.markdown("### 📈 Métricas Gerais")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Alunos", len(df))
            
            with col2:
                if 'Nivel_IAN' in df.columns:
                    severa = len(df[df['Nivel_IAN'] == 'severa'])
                    st.metric("Defasagem Severa", severa)
                else:
                    st.metric("Defasagem Severa", "N/A")
            
            with col3:
                if 'IAN' in df.columns:
                    media_ian = df['IAN'].mean()
                    st.metric("IAN Médio", f"{media_ian:.2f}")
                else:
                    st.metric("IAN Médio", "N/A")
            
            with col4:
                if 'IDA' in df.columns:
                    media_ida = df['IDA'].mean()
                    st.metric("IDA Médio", f"{media_ida:.2f}")
                else:
                    st.metric("IDA Médio", "N/A")
            
            st.markdown("---")
            st.markdown("### 💡 Principais Insights")
            
            insights = []
            
            # Evolução do IAN
            if 'Ano' in df.columns and 'IAN' in df.columns:
                anos = sorted(df['Ano'].unique())
                if len(anos) >= 2:
                    ian_inicial = df[df['Ano'] == anos[0]]['IAN'].mean()
                    ian_final = df[df['Ano'] == anos[-1]]['IAN'].mean()
                    if not pd.isna(ian_inicial) and not pd.isna(ian_final):
                        variacao = ian_final - ian_inicial
                        if variacao > 0:
                            insights.append(f"✅ **Melhoria no IAN:** Aumento de {ian_inicial:.2f} ({anos[0]}) para {ian_final:.2f} ({anos[-1]})")
            
            # Distribuição de risco
            if 'Nivel_IAN' in df.columns:
                nivel_counts = df['Nivel_IAN'].value_counts()
                moderada = nivel_counts.get('moderada', 0)
                em_fase = nivel_counts.get('em fase', 0)
                severa = nivel_counts.get('severa', 0)
                
                total_recuperavel = moderada + em_fase
                pct_recuperavel = (total_recuperavel / len(df) * 100) if len(df) > 0 else 0
                
                insights.append(f"📊 **Distribuição:** {total_recuperavel} alunos ({pct_recuperavel:.1f}%) em situação recuperável ou adequada")
                insights.append(f"⚠️ **Atenção:** {severa} alunos ({severa/len(df)*100:.1f}%) com defasagem severa precisam de intervenção imediata")
            
            # Correlações importantes
            if all(col in df.columns for col in ['IEG', 'IDA']):
                corr_ieg_ida = df['IEG'].corr(df['IDA'])
                if abs(corr_ieg_ida) > 0.3:
                    insights.append(f"🎯 **Engajamento importa:** IEG tem correlação {corr_ieg_ida:.2f} com IDA - programas de engajamento têm alto impacto")
            
            for insight in insights:
                st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📈 Visualizações Rápidas")
            
            # Gráfico de evolução do IAN
            if 'Ano' in df.columns and 'IAN' in df.columns:
                st.markdown("#### Evolução do IAN por Ano")
                ian_anual = df.groupby('Ano')['IAN'].mean().reset_index()
                fig = px.line(
                    ian_anual,
                    x='Ano',
                    y='IAN',
                    title='Evolução da Média do IAN por Ano',
                    markers=True
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=10))
                st.plotly_chart(fig, use_container_width=True)
            
            # Distribuição por nível
            if 'Nivel_IAN' in df.columns:
                st.markdown("#### Distribuição por Nível de Defasagem")
                nivel_counts = df['Nivel_IAN'].value_counts()
                fig = px.pie(
                    values=nivel_counts.values,
                    names=nivel_counts.index,
                    title='Distribuição por Nível de Defasagem',
                    color_discrete_map={
                        'em fase': '#2ecc71',
                        'moderada': '#f39c12',
                        'severa': '#e74c3c'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("## 🔧 Informações Técnicas")
        
        st.markdown("""
        ### Arquitetura do Sistema
        
        **Tecnologias Utilizadas:**
        - **Backend:** Python 3.8+
        - **Framework Web:** Streamlit
        - **Machine Learning:** Scikit-learn
        - **Banco de Dados:** SQLite
        - **Visualização:** Plotly, Matplotlib, Seaborn
        - **Processamento:** Pandas, NumPy
        
        ### Modelo Preditivo
        
        **Algoritmo:** Hist Gradient Boosting Classifier
        
        **Features Utilizadas (14):**
        1. Idade
        2. Ano ingresso
        3. IAA (Índice de Autoavaliação)
        4. IEG (Índice de Engajamento Geral)
        5. IPS (Índice de Perfil Psicossocial)
        6. IPP (Índice de Perfil Psicopedagógico)
        7. IDA (Índice de Desempenho Acadêmico)
        8. IPV (Índice de Ponto de Virada)
        9. Mat (Matemática)
        10. Por (Português)
        11. Ing (Inglês)
        12. Tempo_na_escola (derivada)
        13. Media_academica (derivada)
        14. Media_indicadores (derivada)
        
        **Target:**
        - 0 = Sem risco (IAN == 10)
        - 1 = Em risco (IAN != 10)
        
        ### Performance
        
        - **Acurácia:** 92.4%
        - **ROC-AUC:** 95.7%
        - **F1-Score:** 92-93% (balanceado)
        - **Precision:** ~77%
        - **Recall:** ~85% (em risco)
        
        ### Base de Dados
        
        - **Fonte:** Base oficial Excel da Passos Mágicos
        - **Período:** 2022, 2023, 2024
        - **Total de registros:** ~3.000 alunos
        - **INDE:** Utiliza valores já calculados da base oficial
        
        ### Pré-processamento
        
        1. **Limpeza:** Remoção de duplicatas, tratamento de missing
        2. **Conversão:** Padronização de tipos numéricos
        3. **Feature Engineering:** Criação de features derivadas
        4. **Normalização:** StandardScaler para features numéricas
        5. **Imputação:** Mediana para valores faltantes
        
        ### Separação de Dados
        
        - **Treino:** 75% (stratified)
        - **Teste:** 25% (stratified)
        - **Random State:** 42 (reprodutibilidade)
        """)
    
    with tab5:
        st.markdown("## 📚 Recursos")
        
        st.markdown("""
        ### Funcionalidades Disponíveis
        
        #### 🔮 Predição Individual
        - Faça predições para alunos específicos
        - Visualize probabilidade de risco
        - Receba recomendações personalizadas
        
        #### 📊 Análise de Indicadores
        - Explore cada indicador PEDE em detalhes
        - Visualize evolução temporal
        - Analise correlações e padrões
        
        #### 🤖 Modelo Preditivo
        - Conheça detalhes técnicos do modelo
        - Entenda importância das features
        - Veja métricas de performance
        
        ### Indicadores PEDE Analisados
        
        1. **IAN** - Índice de Adequação de Nível
        2. **IDA** - Índice de Desempenho Acadêmico
        3. **IEG** - Índice de Engajamento Geral
        4. **IAA** - Índice de Autoavaliação
        5. **IPS** - Índice de Perfil Psicossocial
        6. **IPP** - Índice de Perfil Psicopedagógico
        7. **IPV** - Índice de Ponto de Virada
        8. **INDE** - Índice Global (multidimensional)
        
        ### Visualizações Disponíveis
        
        - **Histogramas:** Distribuição dos indicadores
        - **Boxplots:** Comparação entre grupos
        - **Scatter plots:** Relações entre indicadores
        - **Gráficos de linha:** Evolução temporal
        - **Matrizes de correlação:** Relações multidimensionais
        - **Gráficos de barras:** Comparações e rankings
        
        ### Exportação de Dados
        
        Os dados podem ser exportados para análise externa através das tabelas 
        interativas disponíveis em cada seção.
        """)
    
    with tab6:
        st.markdown("## 📖 Como Usar")
        
        st.markdown("""
        ### Guia Rápido
        
        #### 1. Fazer uma Predição
        
        1. Acesse **"Predição Individual de Risco"** no menu lateral
        2. Preencha os dados do aluno:
           - Idade e Ano de ingresso
           - Indicadores PEDE (IAA, IEG, IPS, IPP, IDA, IPV)
           - Notas acadêmicas (Matemática, Português, Inglês)
        3. Clique em **"Prever Risco"**
        4. Visualize o resultado e recomendações
        
        #### 2. Explorar Indicadores
        
        1. Acesse **"Indicadores"** no menu lateral
        2. Selecione o indicador desejado no menu suspenso
        3. Explore os dados e gráficos disponíveis
        4. Analise os insights apresentados
        
        #### 3. Entender o Modelo
        
        1. Acesse **"Modelo Preditivo"** no menu lateral
        2. Veja informações sobre o algoritmo
        3. Entenda as features mais importantes
        4. Analise a performance do modelo
        
        ### Dicas de Uso
        
        - **Filtros:** Use os filtros na sidebar para refinar análises
        - **Gráficos Interativos:** Passe o mouse sobre os gráficos para ver valores detalhados
        - **Tabelas:** Clique nas colunas das tabelas para ordenar
        - **Navegação:** Use o menu lateral para navegar entre seções
        
        ### Interpretação dos Resultados
        
        #### Predição de Risco
        
        - **Probabilidade < 30%:** Baixo risco - acompanhamento regular
        - **Probabilidade 30-70%:** Risco moderado - atenção aumentada
        - **Probabilidade > 70%:** Alto risco - intervenção imediata
        
        #### Indicadores
        
        - **Valores altos (7-10):** Indicadores saudáveis
        - **Valores médios (5-7):** Atenção necessária
        - **Valores baixos (<5):** Intervenção recomendada
        
        ### Suporte
        
        Para dúvidas ou problemas, consulte a seção **"Sobre o Sistema"** ou 
        a documentação técnica disponível.
        """)


def show_indicadores(df, indicador_nome=None):
    """Página única de Indicadores com seletor/abas."""
    st.markdown("## 📊 Indicadores PEDE")
    
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    # Se não foi passado indicador, usa o primeiro como padrão
    if indicador_nome is None:
        indicador_nome = "IAN - Adequação do Nível"
    
    # Roteamento para a análise do indicador selecionado
    if "IAN" in indicador_nome or indicador_nome == "Adequação do Nível":
        show_ian_analysis(df)
    elif "IDA" in indicador_nome or indicador_nome == "Desempenho Acadêmico":
        show_ida_analysis(df)
    elif "IEG" in indicador_nome or indicador_nome == "Engajamento":
        show_ieg_analysis(df)
    elif "IAA" in indicador_nome or indicador_nome == "Autoavaliação":
        show_iaa_analysis(df)
    elif "IPS" in indicador_nome or indicador_nome == "Psicossocial":
        show_ips_analysis(df)
    elif "IPP" in indicador_nome or indicador_nome == "Psicopedagógico":
        show_ipp_analysis(df)
    elif "IPV" in indicador_nome or indicador_nome == "Ponto de Virada":
        show_ipv_analysis(df)
    elif "INDE" in indicador_nome or indicador_nome == "Multidimensionalidade":
        show_inde_analysis(df)
    else:
        # Fallback para IAN
        show_ian_analysis(df)


def show_modelo_preditivo_completo(df):
    """Página completa do Modelo Preditivo."""
    st.markdown("## 🤖 Modelo Preditivo")
    
    model = load_model()
    
    if model is None:
        st.warning("Modelo não disponível. Execute o treinamento primeiro.")
        return
    
    # Abas para organizar conteúdo
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Informações Gerais",
        "🎯 Features e Importância",
        "📈 Performance",
        "💡 Padrões Identificados"
    ])
    
    with tab1:
        st.markdown("### Informações do Modelo")
        
        st.markdown("""
        **Algoritmo:** Hist Gradient Boosting Classifier
        
        **Performance:**
        - Acurácia: ~92%
        - ROC-AUC: ~96%
        - F1-Score: ~92%
        - Precision: ~77%
        - Recall: ~85% (em risco)
        """)
        
        st.markdown("### Definição de Risco")
        
        st.markdown("""
        Um aluno é considerado **em risco** quando:
        - IAN (Índice de Adequação de Nível) ≠ 10
        
        IAN = 10 significa que o aluno está na fase adequada para sua idade.
        """)
        
        st.markdown("### Metodologia")
        
        st.markdown("""
        1. **Base de Dados:** Base oficial Excel da Passos Mágicos (2022-2024)
        2. **Separação:** 75% treino, 25% teste (stratified)
        3. **Pré-processamento:** Imputação de missing (mediana) + Normalização
        4. **Modelos Testados:** Logistic Regression, Random Forest, Hist Gradient Boosting
        5. **Seleção:** Melhor ROC-AUC
        """)
    
    with tab2:
        st.markdown("### Features Utilizadas")
        
        features = [
            'Idade', 'Ano ingresso',
            'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
            'Mat', 'Por', 'Ing', 'IPV',
            'Tempo_na_escola',
            'Media_academica', 'Media_indicadores'
        ]
        
        st.write("**Total de features:** 14")
        st.write("**Features:** " + ", ".join(features))
        
        st.markdown("### Importância das Features")
        
        # Ordem aproximada de importância (baseado em análises anteriores)
        importancia = {
            'Idade': 0.22,
            'IEG': 0.13,
            'Media_academica': 0.07,
            'Ing': 0.03,
            'Ano ingresso': 0.03,
            'IDA': 0.02,
            'IPV': 0.02,
            'Mat': 0.02,
            'Por': 0.02,
            'IPS': 0.01,
            'IAA': 0.01,
            'IPP': 0.01,
            'Tempo_na_escola': 0.01,
            'Media_indicadores': 0.01
        }
        
        df_importancia = pd.DataFrame({
            'Feature': list(importancia.keys()),
            'Importância': list(importancia.values())
        }).sort_values('Importância', ascending=False)
        
        fig = px.bar(
            df_importancia,
            x='Feature',
            y='Importância',
            title='Importância das Features (Permutation Importance)',
            color='Importância',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_importancia, use_container_width=True)
    
    with tab3:
        st.markdown("### Métricas de Performance")
        
        # Carrega dados para modelagem e gera visualizações dinâmicas
        df_modeling = load_data_for_modeling()
        
        if df_modeling is not None and model is not None:
            try:
                # Prepara features e target
                features = [
                    'Idade', 'Ano ingresso',
                    'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
                    'Mat', 'Por', 'Ing', 'IPV',
                    'Tempo_na_escola',
                    'Media_academica', 'Media_indicadores'
                ]
                
                # Verifica se todas as features existem
                available_features = [f for f in features if f in df_modeling.columns]
                
                if len(available_features) == len(features) and 'Risco_defasagem' in df_modeling.columns:
                    X = df_modeling[features]
                    y = df_modeling['Risco_defasagem']
                    
                    # Faz split (mesmo random_state usado no treinamento)
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y,
                        test_size=0.25,
                        random_state=42,
                        stratify=y
                    )
                    
                    # Gera Curva ROC
                    st.markdown("#### 📈 Curva ROC")
                    roc_fig, auc_score = generate_roc_curve(model, X_test, y_test)
                    if roc_fig:
                        st.plotly_chart(roc_fig, use_container_width=True)
                        if auc_score:
                            st.info(f"**AUC-ROC:** {auc_score:.3f}")
                    
                    st.markdown("---")
                    
                    # Gera Matriz de Confusão
                    st.markdown("#### 📊 Matriz de Confusão")
                    cm_fig, metrics = generate_confusion_matrix_plot(model, X_test, y_test)
                    if cm_fig:
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.plotly_chart(cm_fig, use_container_width=True)
                        with col2:
                            if metrics:
                                st.markdown("### Métricas Calculadas")
                                st.metric("Acurácia", f"{metrics['accuracy']:.1%}")
                                st.metric("Precision", f"{metrics['precision']:.1%}")
                                st.metric("Recall", f"{metrics['recall']:.1%}")
                                st.metric("F1-Score", f"{metrics['f1']:.1%}")
                                
                                st.markdown("---")
                                st.markdown("### Detalhes")
                                st.write(f"**Verdadeiros Negativos (TN):** {metrics['tn']}")
                                st.write(f"**Falsos Positivos (FP):** {metrics['fp']}")
                                st.write(f"**Falsos Negativos (FN):** {metrics['fn']}")
                                st.write(f"**Verdadeiros Positivos (TP):** {metrics['tp']}")
                    
                    st.markdown("---")
                    
                    # Métricas resumidas
                    st.markdown("### 📈 Métricas Resumidas")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if metrics:
                            st.metric("Acurácia", f"{metrics['accuracy']:.1%}")
                        else:
                            st.metric("Acurácia", "92.4%")
                    
                    with col2:
                        if auc_score:
                            st.metric("ROC-AUC", f"{auc_score:.1%}")
                        else:
                            st.metric("ROC-AUC", "95.7%")
                    
                    with col3:
                        if metrics:
                            st.metric("F1-Score", f"{metrics['f1']:.1%}")
                        else:
                            st.metric("F1-Score", "92%")
                    
                    with col4:
                        if metrics:
                            st.metric("Recall (Risco)", f"{metrics['recall']:.1%}")
                        else:
                            st.metric("Recall (Risco)", "85%")
                    
                else:
                    st.warning("Dados incompletos para gerar visualizações. Usando métricas estáticas.")
                    # Fallback para métricas estáticas
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Acurácia", "92.4%")
                    with col2:
                        st.metric("ROC-AUC", "95.7%")
                    with col3:
                        st.metric("F1-Score", "92%")
                    with col4:
                        st.metric("Recall (Risco)", "85%")
                    
            except Exception as e:
                st.warning(f"Não foi possível gerar visualizações dinâmicas: {e}")
                st.info("Exibindo métricas estáticas.")
                # Fallback para métricas estáticas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Acurácia", "92.4%")
                with col2:
                    st.metric("ROC-AUC", "95.7%")
                with col3:
                    st.metric("F1-Score", "92%")
                with col4:
                    st.metric("Recall (Risco)", "85%")
        else:
            st.warning("Modelo ou dados não disponíveis. Exibindo métricas estáticas.")
            # Fallback para métricas estáticas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Acurácia", "92.4%")
            with col2:
                st.metric("ROC-AUC", "95.7%")
            with col3:
                st.metric("F1-Score", "92%")
            with col4:
                st.metric("Recall (Risco)", "85%")
        
        st.markdown("---")
        st.markdown("### Comparação de Modelos")
        
        modelos_comparacao = pd.DataFrame({
            'Modelo': ['Hist Gradient Boosting', 'Random Forest', 'Logistic Regression'],
            'AUC-ROC': [0.957, 0.951, 0.755],
            'Acurácia': [0.924, 0.913, 0.675]
        })
        
        st.dataframe(modelos_comparacao, use_container_width=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='AUC-ROC',
            x=modelos_comparacao['Modelo'],
            y=modelos_comparacao['AUC-ROC'],
            marker_color='#1f77b4'
        ))
        fig.add_trace(go.Bar(
            name='Acurácia',
            x=modelos_comparacao['Modelo'],
            y=modelos_comparacao['Acurácia'],
            marker_color='#ff7f0e'
        ))
        fig.update_layout(
            title='Comparação de Modelos',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Padrões Identificados pelo Modelo")
        
        insights = [
            "🎯 **Idade é o fator mais crítico:** Alunos mais velhos têm maior risco de defasagem",
            "📚 **Desempenho acadêmico importa:** Notas baixas (Mat, Por, Ing) aumentam risco",
            "🎓 **Engajamento é crucial:** IEG baixo está associado a maior risco",
            "⏱️ **Tempo na escola:** Alunos com mais tempo na escola podem ter menor risco",
            "📊 **Média de indicadores:** Combinação de indicadores baixos aumenta risco significativamente",
            "🔗 **Relações complexas:** O modelo captura interações não lineares entre features",
            "⚖️ **Balanceamento:** Modelo treinado com class_weight='balanced' para lidar com desbalanceamento"
        ]
        
        for insight in insights:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_sobre_sistema():
    """Página Sobre o Sistema."""
    st.markdown("## ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### Desenvolvimento
    
    Este sistema foi desenvolvido para o **Datathon F5** em parceria com a 
    **Associação Passos Mágicos**.
    
    ### Objetivo
    
    Fornecer uma ferramenta de análise e predição de risco de defasagem educacional 
    para apoiar a tomada de decisão e intervenções pedagógicas personalizadas.
    
    ### Metodologia PEDE
    
    O sistema utiliza os indicadores do **PEDE (Programa de Educação e Desenvolvimento)**:
    
    - **IAN:** Índice de Adequação de Nível
    - **IDA:** Índice de Desempenho Acadêmico
    - **IEG:** Índice de Engajamento Geral
    - **IAA:** Índice de Autoavaliação
    - **IPS:** Índice de Perfil Psicossocial
    - **IPP:** Índice de Perfil Psicopedagógico
    - **IPV:** Índice de Ponto de Virada
    - **INDE:** Índice Global (multidimensional)
    
    ### Base de Dados
    
    - **Fonte:** Base oficial Excel da Passos Mágicos
    - **Período:** 2022, 2023, 2024
    - **Total:** ~3.000 registros de alunos
    - **INDE:** Valores já calculados pela metodologia PEDE oficial
    
    ### Tecnologias
    
    - **Python 3.8+**
    - **Streamlit** - Framework web
    - **Scikit-learn** - Machine Learning
    - **SQLite** - Banco de dados
    - **Plotly** - Visualizações interativas
    - **Pandas/NumPy** - Processamento de dados
    
    ### Estrutura do Projeto
    
    ```
    Datathon_F5/
    ├── app.py                    # Aplicação Streamlit
    ├── src/                      # Código fonte
    │   ├── analise_exploratoria.py
    │   └── modelagem.py
    ├── utils/                    # Utilitários
    │   ├── database.py
    │   └── preprocessing.py
    ├── database/                 # Banco de dados
    │   ├── schema.sql
    │   └── migrate_excel_to_db.py
    ├── models/                   # Modelos treinados
    │   └── modelo_risco_defasagem.pkl
    └── notebooks/                # Notebooks de análise
        └── MODELO_PREDITIVO_DATATHON.ipynb
    ```
    
    ### Limitações e Considerações
    
    - O modelo foi treinado com dados históricos (2022-2024)
    - Performance pode variar com novos dados
    - Recomenda-se re-treinar periodicamente
    - Predições são probabilísticas, não determinísticas
    
    ### Contato e Suporte
    
    Para dúvidas sobre o sistema ou metodologia, consulte a documentação 
    técnica ou entre em contato com a equipe de desenvolvimento.
    
    ### 👥 Autores
    
    Este projeto foi desenvolvido pela equipe de alunos do Tech Challenge 4 - FIAP:
    
    - **Alysson Tenório**
    - **Erico Leopoldino Mota**
    - **Henrique Bruno Oliveira Lima**
    - **Joao Paulo Pinheiro Aguiar**
    - **Laert Valois Rios Carneiro**
    
    ### 📄 Licença
    
    Este projeto foi desenvolvido para fins educacionais como parte do **Datathon - Fase 5 - FIAP**.
    
    ### Créditos
    
    Desenvolvido para o **Datathon F5 - Passos Mágicos**
    
    Associação Passos Mágicos - Transformando vidas através da educação.
    """)


def show_ian_analysis(df):
    """Análise do IAN."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IAN - Índice de Adequação de Nível</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Adequação de Nível (IAN)** mede se o aluno está na fase educacional adequada para sua idade. 
    Este indicador avalia o alinhamento entre a fase em que o aluno se encontra e a fase esperada para sua faixa etária.
    
    **Interpretação:**
    - **IAN = 10:** Aluno está na fase adequada para sua idade (sem defasagem)
    - **IAN < 10:** Aluno apresenta defasagem em relação à fase esperada
    - **IAN < 5:** Defasagem severa
    - **5 ≤ IAN ≤ 7:** Defasagem moderada
    - **IAN > 7:** Aluno adequado ou em fase de recuperação
    """)
    
    # Estatísticas descritivas
    st.markdown("### 📊 Estatísticas Descritivas do IAN")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Média Geral", f"{df['IAN'].mean():.2f}")
    with col2:
        st.metric("Mediana", f"{df['IAN'].median():.2f}")
    with col3:
        st.metric("Desvio Padrão", f"{df['IAN'].std():.2f}")
    with col4:
        st.metric("Total de Alunos", len(df))
    
    # Distribuição do IAN
    st.markdown("### 📈 Distribuição do IAN")
    fig = px.histogram(
        df.dropna(subset=['IAN']),
        x='IAN',
        nbins=10,
        title='Distribuição do Índice de Adequação de Nível (IAN)',
        labels={'IAN': 'IAN', 'count': 'Frequência'},
        template='seaborn'
    )
    fig.update_layout(width=900, height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Evolução anual
    st.markdown("### 📅 Evolução Anual do IAN")
    ian_anual = df.groupby('Ano')['IAN'].agg(['mean', 'std', 'count']).reset_index()
    ian_anual.columns = ['Ano', 'Média', 'Desvio Padrão', 'Quantidade']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(ian_anual, use_container_width=True)
    
    with col2:
        fig = px.line(
            ian_anual,
            x='Ano',
            y='Média',
            title='Evolução da Média do IAN por Ano',
            markers=True
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    # Boxplot por ano
    st.markdown("### 📦 Distribuição Anual (Boxplot)")
    fig = px.box(
        df,
        x='Ano',
        y='IAN',
        title='Distribuição Anual do Índice de Adequação de Nível (IAN)',
        template='seaborn',
        points='outliers'
    )
    fig.update_layout(width=900, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Categorização
    st.markdown("### 🏷️ Distribuição por Nível de Defasagem")
    
    if 'Nivel_IAN' in df.columns:
        nivel_counts = df['Nivel_IAN'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(pd.DataFrame({
                'Nível': nivel_counts.index,
                'Quantidade': nivel_counts.values,
                'Percentual': (nivel_counts.values / len(df) * 100).round(2)
            }), use_container_width=True)
        
        with col2:
            fig = px.pie(
                values=nivel_counts.values,
                names=nivel_counts.index,
                title='Distribuição por Nível de Defasagem',
                color_discrete_map={
                    'em fase': '#2ecc71',
                    'moderada': '#f39c12',
                    'severa': '#e74c3c'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    media_2022 = df[df['Ano'] == 2022]['IAN'].mean() if 2022 in df['Ano'].values else None
    media_2023 = df[df['Ano'] == 2023]['IAN'].mean() if 2023 in df['Ano'].values else None
    media_2024 = df[df['Ano'] == 2024]['IAN'].mean() if 2024 in df['Ano'].values else None
    
    insights = []
    if media_2022 and media_2023 and media_2024:
        melhoria = ((media_2024 - media_2022) / media_2022) * 100
        insights.append(f"✅ **Melhoria consistente:** IAN médio aumentou de {media_2022:.2f} (2022) para {media_2024:.2f} (2024), representando uma melhoria de {melhoria:.1f}%")
    
    if 'Nivel_IAN' in df.columns:
        moderada = len(df[df['Nivel_IAN'] == 'moderada'])
        em_fase = len(df[df['Nivel_IAN'] == 'em fase'])
        severa = len(df[df['Nivel_IAN'] == 'severa'])
        
        insights.append(f"📊 **Distribuição:** {moderada} alunos em defasagem moderada, {em_fase} adequados (em fase), e {severa} com defasagem severa")
        insights.append(f"🎯 **Foco:** A maioria dos alunos ({moderada + em_fase} = {(moderada + em_fase)/len(df)*100:.1f}%) está em situação recuperável ou adequada")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_ida_analysis(df):
    """Análise do IDA."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IDA - Índice de Desempenho Acadêmico</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Desempenho Acadêmico (IDA)** avalia o desempenho do aluno nas atividades acadêmicas, 
    considerando seu rendimento em avaliações, participação em atividades e progresso no aprendizado.
    
    **Interpretação:**
    - **IDA alto (7-10):** Bom desempenho acadêmico, aluno está aprendendo adequadamente
    - **IDA médio (5-7):** Desempenho regular, pode precisar de apoio adicional
    - **IDA baixo (<5):** Desempenho abaixo do esperado, requer intervenção pedagógica
    """)
    
    # Média geral
    st.markdown("### 📊 Média Geral do IDA")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Média Geral", f"{df['IDA'].mean():.2f}")
    with col2:
        st.metric("Mediana", f"{df['IDA'].median():.2f}")
    with col3:
        st.metric("Desvio Padrão", f"{df['IDA'].std():.2f}")
    
    # Evolução por ano
    st.markdown("### 📅 Evolução do IDA por Ano")
    ida_anual = df.groupby('Ano')['IDA'].agg(['mean', 'std']).reset_index()
    ida_anual.columns = ['Ano', 'Média', 'Desvio Padrão']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(ida_anual, use_container_width=True)
    
    with col2:
        fig = px.line(
            ida_anual,
            x='Ano',
            y='Média',
            title='Evolução da Média do IDA por Ano',
            markers=True,
            error_y='Desvio Padrão'
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    # Evolução por fase e ano
    st.markdown("### 📈 Evolução do IDA por Fase e Ano")
    ida_fase_ano = df.groupby(['Ano', 'Fase'])['IDA'].mean().reset_index()
    
    fig = px.line(
        ida_fase_ano,
        x='Ano',
        y='IDA',
        color='Fase',
        title='Evolução do Desempenho Acadêmico Médio (IDA) por Fase e Ano',
        markers=True
    )
    fig.update_traces(mode='markers+lines', line=dict(width=2))
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela detalhada
    st.markdown("### 📋 Tabela Detalhada: IDA por Fase e Ano")
    pivot_ida = df.pivot_table(values='IDA', index='Fase', columns='Ano', aggfunc='mean')
    st.dataframe(pivot_ida.round(2), use_container_width=True)
    
    # Análise de tendência
    st.markdown("### 📊 Análise de Tendência")
    
    # Calcula variação por fase (remove NaN e converte para string)
    fases = sorted([str(f) for f in df['Fase'].dropna().unique()])
    tendencias = []
    
    for fase in fases:
        # Converte Fase para string para comparação consistente
        df_fase = df[df['Fase'].astype(str) == fase]
        if len(df_fase[df_fase['Ano'] == 2022]) > 0 and len(df_fase[df_fase['Ano'] == 2024]) > 0:
            media_2022 = df_fase[df_fase['Ano'] == 2022]['IDA'].mean()
            media_2024 = df_fase[df_fase['Ano'] == 2024]['IDA'].mean()
            variacao = media_2024 - media_2022
            variacao_pct = (variacao / media_2022 * 100) if media_2022 > 0 else 0
            
            tendencia = "📈 Melhorando" if variacao > 0 else "📉 Piorando" if variacao < 0 else "➡️ Estagnado"
            tendencias.append({
                'Fase': fase,
                '2022': f"{media_2022:.2f}",
                '2024': f"{media_2024:.2f}",
                'Variação': f"{variacao:+.2f}",
                'Variação %': f"{variacao_pct:+.1f}%",
                'Tendência': tendencia
            })
    
    if tendencias:
        st.dataframe(pd.DataFrame(tendencias), use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    media_2022 = df[df['Ano'] == 2022]['IDA'].mean() if 2022 in df['Ano'].values else None
    media_2024 = df[df['Ano'] == 2024]['IDA'].mean() if 2024 in df['Ano'].values else None
    
    insights = []
    if media_2022 and media_2024:
        variacao = media_2024 - media_2022
        if variacao > 0:
            insights.append(f"✅ **Melhoria geral:** IDA médio aumentou de {media_2022:.2f} (2022) para {media_2024:.2f} (2024)")
        elif variacao < 0:
            insights.append(f"⚠️ **Queda geral:** IDA médio diminuiu de {media_2022:.2f} (2022) para {media_2024:.2f} (2024)")
        else:
            insights.append(f"➡️ **Estagnado:** IDA médio permaneceu em {media_2022:.2f}")
    
    # Identifica fases com melhor e pior desempenho
    melhor_fase = ida_fase_ano.loc[ida_fase_ano['IDA'].idxmax()]
    pior_fase = ida_fase_ano.loc[ida_fase_ano['IDA'].idxmin()]
    
    insights.append(f"🏆 **Melhor desempenho:** Fase {melhor_fase['Fase']} em {melhor_fase['Ano']} (IDA = {melhor_fase['IDA']:.2f})")
    insights.append(f"⚠️ **Atenção necessária:** Fase {pior_fase['Fase']} em {pior_fase['Ano']} (IDA = {pior_fase['IDA']:.2f})")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_ieg_analysis(df):
    """Análise do IEG."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IEG - Índice de Engajamento Geral</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Engajamento Geral (IEG)** mede o nível de participação, interesse e envolvimento do aluno 
    nas atividades educacionais e do programa. Avalia a motivação e o comprometimento do aluno com o processo de aprendizagem.
    
    **Interpretação:**
    - **IEG alto (7-10):** Aluno altamente engajado, participativo e motivado
    - **IEG médio (5-7):** Engajamento regular, pode variar conforme a atividade
    - **IEG baixo (<5):** Baixo engajamento, pode indicar desmotivação ou dificuldades
    """)
    
    # Correlações
    st.markdown("### 📊 Correlações do IEG")
    
    corr_ieg_ida = df['IEG'].corr(df['IDA'])
    corr_ieg_ipv = df['IEG'].corr(df['IPV'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Correlação IEG × IDA", f"{corr_ieg_ida:.3f}")
        if abs(corr_ieg_ida) > 0.3:
            st.success("✅ Correlação moderada/forte")
        else:
            st.warning("⚠️ Correlação fraca")
    
    with col2:
        st.metric("Correlação IEG × IPV", f"{corr_ieg_ipv:.3f}")
        if abs(corr_ieg_ipv) > 0.3:
            st.success("✅ Correlação moderada/forte")
        else:
            st.warning("⚠️ Correlação fraca")
    
    # Gráfico IEG vs IDA
    st.markdown("### 📈 Relação IEG × IDA")
    fig = px.scatter(
        df,
        x='IEG',
        y='IDA',
        trendline="ols",
        trendline_color_override="red",
        title='Relação entre Índice de Engajamento Geral (IEG) e Desempenho Acadêmico (IDA)',
        labels={'IEG': 'IEG (Engajamento)', 'IDA': 'IDA (Desempenho)'},
        template='plotly_white'
    )
    fig.update_layout(
        title=dict(x=0.5, font_size=16),
        xaxis=dict(showgrid=True, gridcolor='Silver', gridwidth=1),
        yaxis=dict(showgrid=True, gridcolor='Silver', gridwidth=1),
        width=900,
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico IEG vs IPV
    st.markdown("### 📈 Relação IEG × IPV")
    fig = px.scatter(
        df,
        x='IEG',
        y='IPV',
        trendline="ols",
        trendline_color_override="red",
        title='Relação entre Índice de Engajamento Geral (IEG) e Perfil de Vulnerabilidade (IPV)',
        labels={'IEG': 'Engajamento Geral (IEG)', 'IPV': 'Perfil de Vulnerabilidade (IPV)'},
        template='plotly_white'
    )
    fig.update_layout(
        title=dict(x=0.5, font_size=16),
        xaxis=dict(showgrid=True, gridcolor='Silver', gridwidth=1),
        yaxis=dict(showgrid=True, gridcolor='Silver', gridwidth=1),
        width=900,
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise por grupos de engajamento
    st.markdown("### 📊 Desempenho por Nível de Engajamento")
    
    df['IEG_Categoria'] = pd.cut(
        df['IEG'],
        bins=[0, 5, 7, 10],
        labels=['Baixo (0-5)', 'Médio (5-7)', 'Alto (7-10)']
    )
    
    desempenho_por_engajamento = df.groupby('IEG_Categoria').agg({
        'IDA': 'mean',
        'IPV': 'mean',
        'IEG': 'mean'
    }).round(2)
    
    st.dataframe(desempenho_por_engajamento, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    insights = []
    
    if abs(corr_ieg_ida) > 0.3:
        insights.append(f"✅ **Relação positiva:** IEG tem correlação {corr_ieg_ida:.2f} com IDA, indicando que maior engajamento está associado a melhor desempenho")
    else:
        insights.append(f"⚠️ **Relação fraca:** IEG tem correlação {corr_ieg_ida:.2f} com IDA, sugerindo que outros fatores também influenciam o desempenho")
    
    if abs(corr_ieg_ipv) > 0.3:
        insights.append(f"✅ **Relação positiva:** IEG tem correlação {corr_ieg_ipv:.2f} com IPV, indicando que engajamento influencia o ponto de virada")
    else:
        insights.append(f"⚠️ **Relação fraca:** IEG tem correlação {corr_ieg_ipv:.2f} com IPV")
    
    # Compara grupos
    alto_ieg = df[df['IEG_Categoria'] == 'Alto (7-10)']['IDA'].mean()
    baixo_ieg = df[df['IEG_Categoria'] == 'Baixo (0-5)']['IDA'].mean()
    
    if not pd.isna(alto_ieg) and not pd.isna(baixo_ieg):
        diferenca = alto_ieg - baixo_ieg
        insights.append(f"📊 **Impacto do engajamento:** Alunos com alto engajamento têm IDA {diferenca:.2f} pontos maior que alunos com baixo engajamento")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_iaa_analysis(df):
    """Análise do IAA."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IAA - Índice de Autoavaliação</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Autoavaliação (IAA)** reflete a percepção que o aluno tem sobre seu próprio desempenho, 
    engajamento e desenvolvimento. Mede o autoconhecimento e a capacidade de autoavaliação do estudante.
    
    **Interpretação:**
    - **IAA alto (7-10):** Aluno tem percepção positiva de si mesmo e de seu desempenho
    - **IAA médio (5-7):** Autoavaliação moderada, percepção realista ou variável
    - **IAA baixo (<5):** Autoavaliação negativa, pode indicar baixa autoestima ou percepção distorcida
    """)
    
    # Correlações
    corr_iaa_ida = df['IAA'].corr(df['IDA'])
    corr_iaa_ieg = df['IAA'].corr(df['IEG'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Correlação IAA × IDA", f"{corr_iaa_ida:.3f}")
        if abs(corr_iaa_ida) > 0.3:
            st.success("✅ Coerência moderada/forte")
        else:
            st.warning("⚠️ Baixa coerência")
    
    with col2:
        st.metric("Correlação IAA × IEG", f"{corr_iaa_ieg:.3f}")
        if abs(corr_iaa_ieg) > 0.3:
            st.success("✅ Coerência moderada/forte")
        else:
            st.warning("⚠️ Baixa coerência")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='IAA',
            y='IDA',
            trendline="ols",
            trendline_color_override="red",
            title='IAA vs IDA',
            labels={'IAA': 'Autoavaliação (IAA)', 'IDA': 'Desempenho (IDA)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df,
            x='IAA',
            y='IEG',
            trendline="ols",
            trendline_color_override="red",
            title='IAA vs IEG',
            labels={'IAA': 'Autoavaliação (IAA)', 'IEG': 'Engajamento (IEG)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    insights = []
    if abs(corr_iaa_ida) < 0.2:
        insights.append(f"⚠️ **Baixa coerência com desempenho:** IAA tem correlação {corr_iaa_ida:.2f} com IDA, sugerindo que alunos podem não ter percepção precisa de seu desempenho")
    else:
        insights.append(f"✅ **Coerência moderada:** IAA tem correlação {corr_iaa_ida:.2f} com IDA")
    
    if abs(corr_iaa_ieg) < 0.2:
        insights.append(f"⚠️ **Baixa coerência com engajamento:** IAA tem correlação {corr_iaa_ieg:.2f} com IEG")
    else:
        insights.append(f"✅ **Coerência moderada:** IAA tem correlação {corr_iaa_ieg:.2f} com IEG")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_ips_analysis(df):
    """Análise do IPS."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IPS - Índice de Perfil Psicossocial</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Perfil Psicossocial (IPS)** avalia aspectos emocionais, sociais e comportamentais do aluno, 
    incluindo relacionamentos interpessoais, habilidades sociais, bem-estar emocional e adaptação ao ambiente educacional.
    
    **Interpretação:**
    - **IPS alto (7-10):** Perfil psicossocial saudável, boa adaptação social e emocional
    - **IPS médio (5-7):** Perfil psicossocial adequado, com algumas áreas que podem ser desenvolvidas
    - **IPS baixo (<5):** Perfil psicossocial que requer atenção, pode indicar dificuldades emocionais ou sociais
    """)
    
    corr_ips_ida = df['IPS'].corr(df['IDA'])
    corr_ips_ieg = df['IPS'].corr(df['IEG'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Correlação IPS × IDA", f"{corr_ips_ida:.3f}")
    with col2:
        st.metric("Correlação IPS × IEG", f"{corr_ips_ieg:.3f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='IPS',
            y='IDA',
            trendline="ols",
            trendline_color_override="red",
            title='IPS vs IDA',
            labels={'IPS': 'Perfil Psicossocial (IPS)', 'IDA': 'Desempenho (IDA)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df,
            x='IPS',
            y='IEG',
            trendline="ols",
            trendline_color_override="red",
            title='IPS vs IEG',
            labels={'IPS': 'Perfil Psicossocial (IPS)', 'IEG': 'Engajamento (IEG)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    insights = []
    if abs(corr_ips_ida) < 0.2:
        insights.append(f"⚠️ **Relação fraca com desempenho:** IPS tem correlação {corr_ips_ida:.2f} com IDA, indicando que aspectos psicossociais podem não ser preditores diretos de desempenho")
    else:
        insights.append(f"✅ **Relação moderada:** IPS tem correlação {corr_ips_ida:.2f} com IDA")
    
    if corr_ips_ieg < -0.1:
        insights.append(f"⚠️ **Correlação negativa com engajamento:** IPS tem correlação {corr_ips_ieg:.2f} com IEG, sugerindo que problemas psicossociais podem reduzir engajamento")
    else:
        insights.append(f"📊 **Relação:** IPS tem correlação {corr_ips_ieg:.2f} com IEG")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_ipp_analysis(df):
    """Análise do IPP."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IPP - Índice de Perfil Psicopedagógico</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Perfil Psicopedagógico (IPP)** resulta de avaliações psicopedagógicas que analisam aspectos 
    cognitivos, de aprendizagem e desenvolvimento do aluno. Avalia habilidades, dificuldades e potencial de aprendizagem.
    
    **Interpretação:**
    - **IPP alto (7-10):** Perfil psicopedagógico positivo, boas habilidades de aprendizagem
    - **IPP médio (5-7):** Perfil adequado, com áreas que podem ser desenvolvidas
    - **IPP baixo (<5):** Perfil que indica necessidade de apoio psicopedagógico especializado
    """)
    
    corr_ipp_ian = df['IPP'].corr(df['IAN'])
    
    st.metric("Correlação IPP × IAN", f"{corr_ipp_ian:.3f}")
    
    if abs(corr_ipp_ian) > 0.2:
        st.success("✅ Há correlação entre IPP e IAN")
    else:
        st.warning("⚠️ Baixa correlação entre IPP e IAN")
    
    # Boxplot IPP por Nível de IAN
    if 'Nivel_IAN' in df.columns:
        fig = px.box(
            df,
            x='Nivel_IAN',
            y='IPP',
            title='Distribuição de IPP por Nível de IAN',
            labels={'Nivel_IAN': 'Nível de IAN', 'IPP': 'IPP'},
            template='plotly_white',
            color='Nivel_IAN'
        )
        fig.update_layout(
            title=dict(x=0.5, font_size=16),
            yaxis=dict(showgrid=True, gridcolor='Silver', gridwidth=1),
            width=900,
            height=600,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela comparativa
        st.markdown("### 📊 IPP Médio por Nível de IAN")
        ipp_por_nivel = df.groupby('Nivel_IAN')['IPP'].agg(['mean', 'std', 'count']).round(2)
        st.dataframe(ipp_por_nivel, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    insights = []
    if abs(corr_ipp_ian) < 0.2:
        insights.append(f"⚠️ **Baixa correlação:** IPP tem correlação {corr_ipp_ian:.2f} com IAN, sugerindo que avaliações psicopedagógicas podem não confirmar completamente a defasagem identificada pelo IAN")
    else:
        insights.append(f"✅ **Correlação moderada:** IPP tem correlação {corr_ipp_ian:.2f} com IAN, indicando que avaliações psicopedagógicas tendem a confirmar a defasagem")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_ipv_analysis(df):
    """Análise do IPV."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">IPV - Índice de Ponto de Virada</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice de Ponto de Virada (IPV)** identifica momentos críticos ou de transição no desenvolvimento do aluno, 
    onde mudanças significativas podem ocorrer. Avalia a vulnerabilidade ou potencial de transformação do estudante.
    
    **Interpretação:**
    - **IPV alto (7-10):** Aluno em momento de potencial transformação positiva ou baixa vulnerabilidade
    - **IPV médio (5-7):** Situação estável ou em transição moderada
    - **IPV baixo (<5):** Alta vulnerabilidade ou necessidade de intervenção em momento crítico
    """)
    
    # Calcula correlações
    indicadores = ['IDA', 'IEG', 'IPS', 'IAA', 'Mat', 'Por', 'Ing']
    correlacoes_ipv = {}
    
    for ind in indicadores:
        if ind in df.columns:
            correlacoes_ipv[ind] = df['IPV'].corr(df[ind])
    
    # Ordena por valor absoluto
    correlacoes_ordenadas = sorted(correlacoes_ipv.items(), key=lambda x: abs(x[1]), reverse=True)
    
    st.markdown("### 📊 Correlações com IPV (ordenadas por importância)")
    
    df_corr = pd.DataFrame({
        'Indicador': [x[0] for x in correlacoes_ordenadas],
        'Correlação': [x[1] for x in correlacoes_ordenadas]
    })
    
    st.dataframe(df_corr, use_container_width=True)
    
    # Gráfico de barras
    fig = px.bar(
        df_corr,
        x='Indicador',
        y='Correlação',
        title='Correlação de Indicadores com IPV',
        color='Correlação',
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Matriz de correlação
    st.markdown("### 🔥 Matriz de Correlação")
    
    cols_corr = ['IPV'] + [ind for ind in indicadores if ind in df.columns]
    df_corr_matrix = df[cols_corr].corr()
    
    fig = px.imshow(
        df_corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlação - IPV e Indicadores",
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    insights = []
    if correlacoes_ordenadas:
        top1 = correlacoes_ordenadas[0]
        top2 = correlacoes_ordenadas[1] if len(correlacoes_ordenadas) > 1 else None
        
        insights.append(f"🏆 **Maior influência:** {top1[0]} tem correlação {top1[1]:.2f} com IPV, sendo o comportamento mais influente")
        
        if top2:
            insights.append(f"🥈 **Segunda maior influência:** {top2[0]} tem correlação {top2[1]:.2f} com IPV")
        
        # Identifica tipo de comportamento
        academicos = ['IDA', 'Mat', 'Por', 'Ing']
        emocionais = ['IPS', 'IAA']
        engajamento = ['IEG']
        
        top_academico = max([(k, v) for k, v in correlacoes_ipv.items() if k in academicos], key=lambda x: abs(x[1]), default=None)
        top_emocional = max([(k, v) for k, v in correlacoes_ipv.items() if k in emocionais], key=lambda x: abs(x[1]), default=None)
        top_engajamento = max([(k, v) for k, v in correlacoes_ipv.items() if k in engajamento], key=lambda x: abs(x[1]), default=None)
        
        if top_academico:
            insights.append(f"📚 **Comportamento acadêmico mais influente:** {top_academico[0]} (correlação: {top_academico[1]:.2f})")
        if top_engajamento:
            insights.append(f"🎯 **Engajamento mais influente:** {top_engajamento[0]} (correlação: {top_engajamento[1]:.2f})")
        if top_emocional:
            insights.append(f"💭 **Aspecto emocional mais influente:** {top_emocional[0]} (correlação: {top_emocional[1]:.2f})")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_inde_analysis(df):
    """Análise do INDE."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    if 'INDE' not in df.columns:
        st.warning("INDE não disponível nos dados.")
        return
    
    st.markdown('<div class="question-header">INDE - Índice Global (Multidimensional)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Definição
    
    O **Índice Global (INDE)** é um indicador multidimensional que consolida múltiplos aspectos do desenvolvimento 
    educacional do aluno. Combina indicadores acadêmicos, psicossociais, psicopedagógicos e de engajamento para 
    fornecer uma visão integrada do perfil do estudante.
    
    **Interpretação:**
    - **INDE alto (7-10):** Perfil global positivo, desenvolvimento adequado em múltiplas dimensões
    - **INDE médio (5-7):** Perfil adequado, com áreas que podem ser fortalecidas
    - **INDE baixo (<5):** Perfil que requer atenção em múltiplas dimensões do desenvolvimento
    """)
    
    # Correlações individuais
    indicadores = ['IDA', 'IEG', 'IPS', 'IPP']
    correlacoes_inde = {}
    
    for ind in indicadores:
        if ind in df.columns:
            correlacoes_inde[ind] = df['INDE'].corr(df[ind])
    
    st.markdown("### 📊 Correlação Individual com INDE")
    
    df_corr_inde = pd.DataFrame({
        'Indicador': list(correlacoes_inde.keys()),
        'Correlação': list(correlacoes_inde.values())
    }).sort_values('Correlação', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(df_corr_inde, use_container_width=True)
    
    with col2:
        fig = px.bar(
            df_corr_inde,
            x='Indicador',
            y='Correlação',
            title='Correlação de Indicadores com INDE',
            color='Correlação',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Matriz de correlação
    st.markdown("### 🔥 Matriz de Correlação - INDE e Indicadores")
    
    cols_corr = ['INDE'] + [ind for ind in indicadores if ind in df.columns]
    df_corr_matrix = df[cols_corr].corr()
    
    fig = px.imshow(
        df_corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlação - INDE e Indicadores",
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise combinada
    st.markdown("### 📈 Análise Combinada")
    
    # Cria grupos baseados em quartis (com tratamento para valores duplicados)
    for ind in indicadores:
        if ind in df.columns:
            try:
                # Remove NaN antes de criar quartis
                df_clean = df[ind].dropna()
                if len(df_clean) >= 4:  # Precisa de pelo menos 4 valores para quartis
                    df[f'{ind}_Quartil'] = pd.qcut(
                        df_clean, 
                        q=4, 
                        labels=['Q1', 'Q2', 'Q3', 'Q4'],
                        duplicates='drop'
                    )
            except (ValueError, Exception):
                # Se qcut falhar, usa cut com bins definidos manualmente
                try:
                    df_clean = df[ind].dropna()
                    if len(df_clean) > 0:
                        bins = pd.cut(
                            df_clean,
                            bins=4,
                            labels=['Q1', 'Q2', 'Q3', 'Q4'],
                            duplicates='drop'
                        )
                        df.loc[df_clean.index, f'{ind}_Quartil'] = bins
                except Exception:
                    # Se ainda falhar, pula este indicador
                    pass
    
    # Combinações
    st.markdown("#### INDE Médio por Quartis dos Indicadores")
    
    insights = []
    if correlacoes_inde:
        top_ind = max(correlacoes_inde.items(), key=lambda x: abs(x[1]))
        insights.append(f"🏆 **Indicador mais influente no INDE:** {top_ind[0]} com correlação {top_ind[1]:.2f}")
        
        # Ordena por correlação
        ordenados = sorted(correlacoes_inde.items(), key=lambda x: abs(x[1]), reverse=True)
        insights.append(f"📊 **Ordem de influência:** {', '.join([f'{k} ({v:.2f})' for k, v in ordenados])}")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_model_analysis(df):
    """Pergunta 9: Análise do Modelo Preditivo."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">9. Previsão de risco com Machine Learning: Quais padrões nos indicadores permitem identificar alunos em risco antes de queda no desempenho ou aumento da defasagem?</div>', unsafe_allow_html=True)
    
    model = load_model()
    
    if model is None:
        st.warning("Modelo não disponível. Execute o treinamento primeiro.")
        return
    
    st.markdown("### 🤖 Informações do Modelo")
    
    st.markdown("""
    **Algoritmo:** Hist Gradient Boosting Classifier
    
    **Performance:**
    - Acurácia: ~92%
    - ROC-AUC: ~96%
    - F1-Score: ~92%
    """)
    
    st.markdown("### 📊 Features Mais Importantes")
    
    # Features utilizadas
    features = [
        'Idade', 'Ano ingresso',
        'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
        'Mat', 'Por', 'Ing', 'IPV',
        'Tempo_na_escola',
        'Media_academica', 'Media_indicadores'
    ]
    
    st.markdown("**Features utilizadas:**")
    st.write(", ".join(features))
    
    st.markdown("### 💡 Principais Padrões Identificados")
    
    insights = [
        "🎯 **Idade é o fator mais crítico:** Alunos mais velhos têm maior risco de defasagem",
        "📚 **Desempenho acadêmico importa:** Notas baixas (Mat, Por, Ing) aumentam risco",
        "🎓 **Engajamento é crucial:** IEG baixo está associado a maior risco",
        "⏱️ **Tempo na escola:** Alunos com mais tempo na escola podem ter menor risco",
        "📊 **Média de indicadores:** Combinação de indicadores baixos aumenta risco significativamente"
    ]
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔮 Use a página 'Predição Individual' para testar o modelo!")


def show_effectiveness_analysis(df):
    """Pergunta 10: Efetividade do Programa."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">10. Efetividade do programa: Os indicadores mostram melhora consistente ao longo do ciclo nas diferentes fases (Quartzo, Ágata, Ametista e Topázio), confirmando o impacto real do programa?</div>', unsafe_allow_html=True)
    
    # Mapeia fases para categorias (se disponível)
    # Assumindo que fases numéricas representam progressão
    
    st.markdown("### 📈 Evolução dos Indicadores Principais")
    
    # Agrupa por ano
    indicadores_principais = ['IAN', 'IDA', 'IEG', 'IPV']
    if 'INDE' in df.columns:
        indicadores_principais.append('INDE')
    
    evolucao_anual = df.groupby('Ano')[indicadores_principais].mean()
    
    st.dataframe(evolucao_anual.round(2), use_container_width=True)
    
    # Gráfico de evolução
    fig = go.Figure()
    
    for ind in indicadores_principais:
        if ind in evolucao_anual.columns:
            fig.add_trace(go.Scatter(
                x=evolucao_anual.index,
                y=evolucao_anual[ind],
                mode='lines+markers',
                name=ind,
                line=dict(width=3)
            ))
    
    fig.update_layout(
        title='Evolução dos Indicadores Principais por Ano',
        xaxis_title='Ano',
        yaxis_title='Valor Médio',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise por fase
    if 'Fase' in df.columns:
        st.markdown("### 📊 Evolução por Fase")
        
        # Agrupa por fase e ano
        evolucao_fase = df.groupby(['Fase', 'Ano'])[indicadores_principais].mean().reset_index()
        
        for ind in indicadores_principais:
            if ind in evolucao_fase.columns:
                fig = px.line(
                    evolucao_fase,
                    x='Ano',
                    y=ind,
                    color='Fase',
                    title=f'Evolução de {ind} por Fase e Ano',
                    markers=True
                )
                fig.update_traces(mode='markers+lines', line=dict(width=2))
                st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("### 💡 Principais Insights")
    
    insights = []
    
    # Calcula variação 2022-2024
    if 2022 in df['Ano'].values and 2024 in df['Ano'].values:
        for ind in indicadores_principais:
            if ind in df.columns:
                media_2022 = df[df['Ano'] == 2022][ind].mean()
                media_2024 = df[df['Ano'] == 2024][ind].mean()
                
                if not pd.isna(media_2022) and not pd.isna(media_2024):
                    variacao = media_2024 - media_2022
                    variacao_pct = (variacao / media_2022 * 100) if media_2022 > 0 else 0
                    
                    if variacao > 0:
                        insights.append(f"✅ **{ind} melhorou:** {media_2022:.2f} (2022) → {media_2024:.2f} (2024) = +{variacao_pct:.1f}%")
                    elif variacao < 0:
                        insights.append(f"⚠️ **{ind} diminuiu:** {media_2022:.2f} (2022) → {media_2024:.2f} (2024) = {variacao_pct:.1f}%")
    
    if not insights:
        insights.append("📊 Analise os gráficos acima para identificar tendências de melhoria")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_creative_insights(df):
    """Pergunta 11: Insights Criativos."""
    if df is None:
        st.error("Erro ao carregar dados.")
        return
    
    st.markdown('<div class="question-header">11. Insights e criatividade: Você pode adicionar mais insights e pontos de vista não abordados nas perguntas, utilize a criatividade para a Passos Mágicos.</div>', unsafe_allow_html=True)
    
    st.markdown("### 💡 Insights Criativos e Recomendações")
    
    insights = []
    
    # 1. Análise de perfil de risco
    if 'Nivel_IAN' in df.columns and 'IEG' in df.columns:
        alto_risco = df[df['Nivel_IAN'] == 'severa']
        if len(alto_risco) > 0:
            ieg_alto_risco = alto_risco['IEG'].mean()
            ieg_geral = df['IEG'].mean()
            
            if not pd.isna(ieg_alto_risco) and not pd.isna(ieg_geral):
                insights.append(f"🎯 **Perfil de alto risco:** Alunos com defasagem severa têm IEG médio de {ieg_alto_risco:.2f} vs {ieg_geral:.2f} geral. **Recomendação:** Intervenções focadas em engajamento para este grupo")
    
    # 2. Análise de idade
    if 'Idade' in df.columns and 'IAN' in df.columns:
        idade_ian = df.groupby('Idade')['IAN'].mean().reset_index()
        idade_risco = idade_ian.loc[idade_ian['IAN'].idxmin()]
        
        insights.append(f"⚠️ **Idade crítica:** Idade {idade_risco['Idade']:.0f} anos apresenta menor IAN médio ({idade_risco['IAN']:.2f}). **Recomendação:** Atenção especial para alunos nesta faixa etária")
    
    # 3. Análise de disciplinas
    if all(col in df.columns for col in ['Mat', 'Por', 'Ing', 'IAN']):
        mat_corr = df['Mat'].corr(df['IAN'])
        por_corr = df['Por'].corr(df['IAN'])
        ing_corr = df['Ing'].corr(df['IAN'])
        
        disciplinas = [
            ('Matemática', mat_corr),
            ('Português', por_corr),
            ('Inglês', ing_corr)
        ]
        
        disciplina_mais_importante = max(disciplinas, key=lambda x: abs(x[1]))
        insights.append(f"📚 **Disciplina mais crítica:** {disciplina_mais_importante[0]} tem maior correlação com IAN ({disciplina_mais_importante[1]:.2f}). **Recomendação:** Reforço prioritário nesta disciplina")
    
    # 4. Análise de combinação de indicadores
    if all(col in df.columns for col in ['IEG', 'IDA', 'IAN']):
        # Alunos com IEG e IDA altos
        alto_ieg_ida = df[(df['IEG'] > df['IEG'].quantile(0.75)) & (df['IDA'] > df['IDA'].quantile(0.75))]
        if len(alto_ieg_ida) > 0:
            ian_alto = alto_ieg_ida['IAN'].mean()
            ian_geral = df['IAN'].mean()
            
            if not pd.isna(ian_alto) and not pd.isna(ian_geral):
                insights.append(f"✅ **Combinando forças:** Alunos com IEG e IDA altos têm IAN médio de {ian_alto:.2f} vs {ian_geral:.2f} geral. **Recomendação:** Estratégias que combinam engajamento e desempenho são mais efetivas")
    
    # 5. Análise temporal
    if 'Ano' in df.columns and 'IAN' in df.columns:
        anos = sorted(df['Ano'].unique())
        if len(anos) >= 2:
            variacao_total = df[df['Ano'] == anos[-1]]['IAN'].mean() - df[df['Ano'] == anos[0]]['IAN'].mean()
            if variacao_total > 0:
                insights.append(f"📈 **Tendência positiva:** IAN melhorou {variacao_total:.2f} pontos entre {anos[0]} e {anos[-1]}. **Recomendação:** Manter estratégias atuais e intensificar para grupos de risco")
    
    # 6. Recomendações gerais
    st.markdown("### 🎯 Recomendações Estratégicas")
    
    recomendacoes = [
        "**1. Intervenção Precoce:** Use o modelo preditivo para identificar alunos em risco antes que a defasagem se agrave",
        "**2. Foco em Engajamento:** IEG tem forte correlação com desempenho - programas de engajamento podem ter alto impacto",
        "**3. Acompanhamento Personalizado:** Alunos com múltiplos indicadores baixos precisam de atenção individualizada",
        "**4. Monitoramento Contínuo:** Acompanhe evolução dos indicadores ao longo do ano, não apenas no final",
        "**5. Combinação de Indicadores:** Estratégias que trabalham múltiplos indicadores simultaneamente são mais efetivas",
        "**6. Idade como Fator Crítico:** Alunos mais velhos precisam de abordagens diferenciadas",
        "**7. Disciplinas Prioritárias:** Identifique e priorize reforço nas disciplinas com maior correlação com defasagem"
    ]
    
    for rec in recomendacoes:
        st.markdown(f'<div class="insight-box">{rec}</div>', unsafe_allow_html=True)
    
    if insights:
        st.markdown("### 📊 Insights Adicionais")
        for insight in insights:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def show_prediction():
    """Página de predição individual (mantém código original)."""
    st.markdown("## 🔮 Predição Individual de Risco")
    
    model = load_model()
    if model is None:
        st.error("Modelo não disponível. Por favor, verifique se o modelo foi treinado.")
        return
    
    st.markdown("### Preencha os dados do aluno:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.number_input("Idade", min_value=5, max_value=25, value=12, step=1)
        ano_ingresso = st.number_input("Ano de Ingresso", min_value=2010, max_value=2024, value=2020, step=1)
        
        st.markdown("#### Indicadores PEDE (0-10):")
        iaa = st.slider("IAA - Autoavaliação", 0.0, 10.0, 7.0, 0.1)
        ieg = st.slider("IEG - Engajamento", 0.0, 10.0, 7.0, 0.1)
        ips = st.slider("IPS - Psicossocial", 0.0, 10.0, 7.0, 0.1)
        ipp = st.slider("IPP - Psicopedagógico", 0.0, 10.0, 7.0, 0.1)
        ida = st.slider("IDA - Desempenho Acadêmico", 0.0, 10.0, 7.0, 0.1)
        ipv = st.slider("IPV - Ponto de Virada", 0.0, 10.0, 7.0, 0.1)
    
    with col2:
        st.markdown("#### Notas Acadêmicas (0-10):")
        mat = st.slider("Matemática", 0.0, 10.0, 7.0, 0.1)
        por = st.slider("Português", 0.0, 10.0, 7.0, 0.1)
        ing = st.slider("Inglês", 0.0, 10.0, 7.0, 0.1)
    
    ano_atual = 2024
    tempo_na_escola = ano_atual - ano_ingresso
    media_academica = (mat + por + ing) / 3.0
    media_indicadores = (iaa + ieg + ips + ipp + ida + ipv) / 6.0
    
    if st.button("🔮 Prever Risco", type="primary"):
        features = [
            'Idade', 'Ano ingresso',
            'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
            'Mat', 'Por', 'Ing', 'IPV',
            'Tempo_na_escola',
            'Media_academica', 'Media_indicadores'
        ]
        
        input_data = pd.DataFrame({
            'Idade': [idade],
            'Ano ingresso': [ano_ingresso],
            'IAA': [iaa],
            'IEG': [ieg],
            'IPS': [ips],
            'IPP': [ipp],
            'IDA': [ida],
            'Mat': [mat],
            'Por': [por],
            'Ing': [ing],
            'IPV': [ipv],
            'Tempo_na_escola': [tempo_na_escola],
            'Media_academica': [media_academica],
            'Media_indicadores': [media_indicadores]
        })
        
        try:
            probabilidade = model.predict_proba(input_data)[0][1]
            risco = model.predict(input_data)[0]
            
            st.markdown("---")
            st.markdown("## 📊 Resultado da Predição")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Probabilidade de Risco", f"{probabilidade:.1%}")
            
            with col2:
                status = "🔴 Em Risco" if risco == 1 else "🟢 Sem Risco"
                st.metric("Classificação", status)
            
            with col3:
                confianca = probabilidade if risco == 1 else (1 - probabilidade)
                st.metric("Confiança", f"{confianca:.1%}")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Sem Risco', 'Em Risco'],
                y=[1 - probabilidade, probabilidade],
                marker_color=['green', 'red'],
                text=[f"{(1-probabilidade):.1%}", f"{probabilidade:.1%}"],
                textposition='auto'
            ))
            fig.update_layout(
                title="Probabilidade de Risco",
                yaxis_title="Probabilidade",
                yaxis_range=[0, 1],
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 💡 Recomendações")
            if risco == 1:
                st.warning("""
                **Aluno em Risco de Defasagem**
                
                Recomendações:
                - Acompanhamento individualizado
                - Reforço nas áreas com menor desempenho
                - Apoio psicopedagógico
                - Monitoramento contínuo dos indicadores
                """)
            else:
                st.success("""
                **Aluno Sem Risco de Defasagem**
                
                Mantenha:
                - Acompanhamento regular
                - Incentivo ao engajamento
                - Monitoramento dos indicadores
                """)
            
        except Exception as e:
            st.error(f"Erro ao fazer predição: {e}")


if __name__ == "__main__":
    main()
