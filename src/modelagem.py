"""
Módulo de Modelagem Preditiva
Consolida todo o código de modelagem realizado nos notebooks.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional
import warnings

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_auc_score,
    RocCurveDisplay,
    precision_recall_curve
)
from sklearn.inspection import permutation_importance

from utils.database import get_db_manager

warnings.filterwarnings('ignore')


class ModelagemPreditiva:
    """Classe para realizar modelagem preditiva de risco de defasagem."""
    
    def __init__(self, random_state: int = 42):
        """
        Inicializa a modelagem preditiva.
        
        Args:
            random_state: Seed para reprodutibilidade
        """
        self.db = get_db_manager()
        self.random_state = random_state
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.preprocessor = None
        self.results = {}
        self.features = [
            'Idade', 'Ano ingresso',
            'IAA', 'IEG', 'IPS', 'IPP', 'IDA',
            'Mat', 'Por', 'Ing', 'IPV',
            'Tempo_na_escola',
            'Media_academica', 'Media_indicadores'
        ]
    
    def carregar_dados(self):
        """Carrega dados do banco para modelagem."""
        print("Carregando dados do banco de dados...")
        self.df = self.db.load_data_for_modeling()
        
        # Seleciona features e target
        self.X = self.df[self.features].copy()
        self.y = self.df['Risco_defasagem'].copy()
        
        print(f"Dados carregados: {len(self.df)} registros")
        print(f"Features: {len(self.features)}")
        print(f"Distribuição do target:")
        print(self.y.value_counts())
        
        return self.df
    
    def preparar_dados(self, test_size: float = 0.25):
        """
        Prepara dados para treinamento e teste.
        
        Args:
            test_size: Proporção dos dados para teste
        """
        print("\nPreparando dados para treinamento e teste...")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y,
            test_size=test_size,
            random_state=self.random_state,
            stratify=self.y
        )
        
        print(f"Treino: {len(self.X_train)} registros")
        print(f"Teste: {len(self.X_test)} registros")
        print(f"Proporção treino/teste: {1-test_size:.0%}/{test_size:.0%}")
    
    def criar_preprocessor(self):
        """Cria pipeline de pré-processamento."""
        print("\nCriando pipeline de pré-processamento...")
        
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.features)
            ]
        )
        
        print("Pipeline de pré-processamento criado")
    
    def treinar_modelos(self):
        """Treina múltiplos modelos e seleciona o melhor."""
        print("\n" + "="*60)
        print("TREINANDO MODELOS")
        print("="*60)
        
        if self.preprocessor is None:
            self.criar_preprocessor()
        
        # Define modelos
        self.models = {
            'Logistic Regression': LogisticRegression(
                class_weight='balanced',
                max_iter=1000,
                random_state=self.random_state
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=300,
                class_weight='balanced',
                random_state=self.random_state
            ),
            'Hist Gradient Boosting': HistGradientBoostingClassifier(
                max_iter=300,
                learning_rate=0.05,
                random_state=self.random_state
            )
        }
        
        results = []
        
        for name, model in self.models.items():
            print(f"\n--- Treinando {name} ---")
            
            pipe = Pipeline(steps=[
                ('preprocessor', self.preprocessor),
                ('model', model)
            ])
            
            # Treina
            pipe.fit(self.X_train, self.y_train)
            
            # Predições
            y_pred = pipe.predict(self.X_test)
            y_prob = pipe.predict_proba(self.X_test)[:, 1]
            
            # Métricas
            acc = accuracy_score(self.y_test, y_pred)
            roc = roc_auc_score(self.y_test, y_prob)
            
            results.append((name, acc, roc, pipe))
            
            print(f"Acurácia: {acc:.3f}")
            print(f"ROC-AUC: {roc:.3f}")
            print(classification_report(self.y_test, y_pred, target_names=['Sem risco', 'Em risco']))
        
        # Seleciona melhor modelo (baseado em ROC-AUC)
        self.best_model_name = max(results, key=lambda x: x[2])[0]
        self.best_model = max(results, key=lambda x: x[2])[3]
        
        print("\n" + "="*60)
        print(f"MELHOR MODELO: {self.best_model_name}")
        print("="*60)
        
        # Salva resultados
        self.results['modelos'] = {
            name: {'acc': acc, 'roc': roc}
            for name, acc, roc, _ in results
        }
        self.results['melhor_modelo'] = self.best_model_name
        
        return self.best_model
    
    def avaliar_modelo(self):
        """Avalia o melhor modelo com métricas detalhadas."""
        print("\n" + "="*60)
        print("AVALIANDO MELHOR MODELO")
        print("="*60)
        
        y_pred = self.best_model.predict(self.X_test)
        y_prob = self.best_model.predict_proba(self.X_test)[:, 1]
        
        # Métricas
        acc = accuracy_score(self.y_test, y_pred)
        roc = roc_auc_score(self.y_test, y_prob)
        
        # Classification report
        report = classification_report(
            self.y_test, y_pred,
            target_names=['Sem risco', 'Em risco'],
            output_dict=True
        )
        
        # Matriz de confusão
        cm = confusion_matrix(self.y_test, y_pred)
        
        self.results['avaliacao'] = {
            'acuracia': acc,
            'roc_auc': roc,
            'classification_report': report,
            'confusion_matrix': cm.tolist()
        }
        
        print(f"Acurácia: {acc:.3f}")
        print(f"ROC-AUC: {roc:.3f}")
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred, target_names=['Sem risco', 'Em risco']))
        
        return self.results['avaliacao']
    
    def analisar_importancia_features(self):
        """Analisa importância das features usando permutation importance."""
        print("\n" + "="*60)
        print("ANALISANDO IMPORTÂNCIA DAS FEATURES")
        print("="*60)
        
        r = permutation_importance(
            self.best_model,
            self.X_test,
            self.y_test,
            n_repeats=10,
            random_state=self.random_state,
            scoring='roc_auc'
        )
        
        importance_df = pd.DataFrame({
            'Feature': self.features,
            'Importância': r.importances_mean
        }).sort_values(by='Importância', ascending=False)
        
        print("\nImportância das Features (Permutation Importance):")
        for idx, row in importance_df.iterrows():
            print(f"  {row['Feature']}: {row['Importância']:.4f}")
        
        self.results['importancia_features'] = importance_df.to_dict('records')
        
        return importance_df
    
    def salvar_modelo(self, caminho: Optional[str] = None):
        """
        Salva o modelo treinado.
        
        Args:
            caminho: Caminho para salvar o modelo (None = padrão)
        """
        if caminho is None:
            caminho = Path('models') / 'modelo_risco_defasagem.pkl'
        
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho, 'wb') as f:
            pickle.dump(self.best_model, f)
        
        print(f"\nModelo salvo em: {caminho}")
        self.results['caminho_modelo'] = str(caminho)
    
    def gerar_visualizacoes(self, salvar: bool = False, diretorio: str = 'output'):
        """
        Gera visualizações do modelo.
        
        Args:
            salvar: Se True, salva as visualizações
            diretorio: Diretório para salvar (se salvar=True)
        """
        import os
        
        if salvar:
            os.makedirs(diretorio, exist_ok=True)
        
        # 1. Curva ROC
        RocCurveDisplay.from_estimator(
            self.best_model,
            self.X_test,
            self.y_test
        )
        plt.title(f"Curva ROC - {self.best_model_name}")
        if salvar:
            plt.savefig(f'{diretorio}/curva_roc.png', dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
        
        # 2. Matriz de Confusão
        y_pred = self.best_model.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=['Sem risco', 'Em risco']
        )
        disp.plot(cmap='Blues')
        plt.title(f"Matriz de Confusão - {self.best_model_name}")
        if salvar:
            plt.savefig(f'{diretorio}/matriz_confusao.png', dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
        
        # 3. Importância das Features
        importance_df = self.analisar_importancia_features()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=importance_df, x='Importância', y='Feature')
        plt.title('Permutation Importance das Variáveis (ROC-AUC)')
        plt.tight_layout()
        if salvar:
            plt.savefig(f'{diretorio}/importancia_features.png', dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
        
        print(f"\nVisualizações geradas{' e salvas' if salvar else ''}")
    
    def executar_pipeline_completo(self, salvar_modelo: bool = True, salvar_visualizacoes: bool = True):
        """
        Executa pipeline completo de modelagem.
        
        Args:
            salvar_modelo: Se True, salva o modelo treinado
            salvar_visualizacoes: Se True, salva as visualizações
        """
        print("\n" + "="*60)
        print("PIPELINE COMPLETO DE MODELAGEM")
        print("="*60)
        
        # 1. Carregar dados
        self.carregar_dados()
        
        # 2. Preparar dados
        self.preparar_dados()
        
        # 3. Criar preprocessor
        self.criar_preprocessor()
        
        # 4. Treinar modelos
        self.treinar_modelos()
        
        # 5. Avaliar modelo
        self.avaliar_modelo()
        
        # 6. Analisar importância
        self.analisar_importancia_features()
        
        # 7. Salvar modelo
        if salvar_modelo:
            self.salvar_modelo()
        
        # 8. Gerar visualizações
        if salvar_visualizacoes:
            self.gerar_visualizacoes(salvar=True, diretorio='output/modelagem')
        
        print("\n" + "="*60)
        print("PIPELINE CONCLUÍDO COM SUCESSO!")
        print("="*60)
        
        return self.results


def main():
    """Função principal para executar modelagem."""
    modelagem = ModelagemPreditiva()
    resultados = modelagem.executar_pipeline_completo()
    
    return modelagem, resultados


if __name__ == '__main__':
    modelagem, resultados = main()
