from pathlib import Path
from typing import Dict, Any
from src.utils.data_exporter import DataExporter
from src.visualization.dashboard import StyleDashboard
from src.api.prediction_service import PredictionService

class StylometricAnalysisApp:
    def __init__(self):
        # ... existing initialization ...
        self.data_exporter = DataExporter()
        self.dashboard = StyleDashboard()
        self.prediction_service = PredictionService('models/style_classifier.joblib')
    
    async def analyze_and_predict(self, pdf_path: str) -> Dict[str, Any]:
        # Get basic analysis
        analysis_results = self.analyze_document(pdf_path)
        
        # Export for training
        self.data_exporter.export_for_training(analysis_results, Path(pdf_path).name)
        
        # Get AI predictions
        predictions = await self.prediction_service.predict_style(analysis_results)
        
        # Combine results
        analysis_results['predictions'] = predictions.dict()
        
        # Visualize results
        self.dashboard.visualize_analysis(analysis_results)
        
        return analysis_results 