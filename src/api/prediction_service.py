from pydantic import BaseModel
from typing import Dict, Any
import joblib
import numpy as np
from pathlib import Path
from src.ml.feature_processor import FeatureProcessor

class StylePrediction(BaseModel):
    style_classification: str
    confidence_score: float
    writing_patterns: Dict[str, str]
    recommendations: list[str]

class PredictionService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        try:
            if Path(model_path).exists():
                self.model = joblib.load(model_path)
        except Exception:
            pass
        self.feature_processor = FeatureProcessor()
    
    def predict_style(self, analysis_results: Dict[str, Any]) -> StylePrediction:
        try:
            # If no model is available, return default predictions
            if self.model is None:
                return StylePrediction(
                    style_classification=analysis_results['analysis']['style_metrics']['classification'],
                    confidence_score=1.0,
                    writing_patterns=analysis_results['analysis']['writing_patterns'],
                    recommendations=self._generate_default_recommendations(analysis_results)
                )

            # Process features
            features = self.feature_processor.prepare_features_for_prediction(analysis_results)
            
            # Get model prediction
            prediction = self.model.predict_proba(features)[0]
            predicted_class = self.model.classes_[np.argmax(prediction)]
            confidence = np.max(prediction)
            
            return StylePrediction(
                style_classification=predicted_class,
                confidence_score=float(confidence),
                writing_patterns=analysis_results['analysis']['writing_patterns'],
                recommendations=self._generate_recommendations(analysis_results, predicted_class)
            )
            
        except Exception as e:
            # Return default predictions on error
            return StylePrediction(
                style_classification=analysis_results['analysis']['style_metrics']['classification'],
                confidence_score=1.0,
                writing_patterns=analysis_results['analysis']['writing_patterns'],
                recommendations=self._generate_default_recommendations(analysis_results)
            )

    def _generate_default_recommendations(self, analysis_results: Dict[str, Any]) -> list[str]:
        """Generate default recommendations based on analysis results."""
        recommendations = []
        
        # Add recommendations based on readability scores
        if analysis_results['analysis']['readability']['flesch_reading_ease'] < 50:
            recommendations.append("Consider simplifying your language for better readability")
            
        # Add recommendations based on structural analysis
        if analysis_results['analysis']['structural_analysis']['structure_consistency'] < 0.5:
            recommendations.append("Work on maintaining consistent paragraph lengths")
            
        # Add recommendations based on syntactic analysis
        if analysis_results['analysis']['syntactic_analysis']['sentence_complexity'] > 100:
            recommendations.append("Consider breaking down complex sentences")
            
        # Add default recommendation if none were generated
        if not recommendations:
            recommendations.append("Your writing style appears balanced")
            
        return recommendations