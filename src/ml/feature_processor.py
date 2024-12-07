import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple, Dict, Any
import numpy as np

class FeatureProcessor:
    """Processes stylometric features for ML training."""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepare features for ML training."""
        # Encode categorical variables
        categorical_columns = ['style_classification', 'vocabulary_usage', 
                             'sentence_structure', 'text_organization']
        
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            df[col + '_encoded'] = self.label_encoders[col].fit_transform(df[col])
        
        # Separate features and target
        feature_columns = [
            'style_complexity', 'style_consistency', 'flesch_reading_ease',
            'gunning_fog', 'vocabulary_richness', 'type_token_ratio',
            'sentence_complexity', 'syntactic_diversity'
        ] + [col + '_encoded' for col in categorical_columns]
        
        X = df[feature_columns]
        y = df['style_classification_encoded']
        
        # Scale features
        X_scaled = pd.DataFrame(
            self.scaler.fit_transform(X),
            columns=X.columns
        )
        
        return X_scaled, y 
    
    def prepare_features_for_prediction(self, analysis_results: Dict[str, Any]) -> np.ndarray:
        """Prepare features for prediction from analysis results."""
        # Extract relevant features
        features = {
            'style_complexity': analysis_results['analysis']['style_metrics']['complexity']['score'],
            'style_consistency': analysis_results['analysis']['style_metrics']['consistency']['score'],
            'flesch_reading_ease': analysis_results['analysis']['readability']['flesch_reading_ease'],
            'gunning_fog': analysis_results['analysis']['readability']['gunning_fog'],
            'vocabulary_richness': analysis_results['analysis']['lexical_analysis']['vocabulary_richness'],
            'type_token_ratio': analysis_results['analysis']['lexical_analysis']['type_token_ratio'],
            'sentence_complexity': analysis_results['analysis']['syntactic_analysis']['sentence_complexity'],
            'syntactic_diversity': analysis_results['analysis']['syntactic_analysis']['syntactic_diversity']
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(df)
        
        return X_scaled