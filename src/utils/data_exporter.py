from typing import Dict, Any
import pandas as pd
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    """Handles export of analysis results for ML training and visualization."""
    
    def __init__(self, output_dir: str = 'data'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def export_for_training(self, results: Dict[str, Any], filename: str) -> str:
        """Export results in a format suitable for ML training."""
        try:
            # Safely extract nested values with defaults
            analysis = results.get('analysis', {})
            style_metrics = analysis.get('style_metrics', {})
            complexity = style_metrics.get('complexity', {})
            consistency = style_metrics.get('consistency', {})
            writing_patterns = analysis.get('writing_patterns', {})
            readability = results.get('readability_metrics', {})
            lexical = results.get('lexical_features', {})
            syntactic = results.get('syntactic_features', {})

            # Flatten nested dictionaries for ML
            flat_data = {
                'document_id': filename,
                'style_complexity': complexity.get('score', 0.0),
                'style_consistency': consistency.get('score', 0.0),
                'style_classification': style_metrics.get('classification', 'Unknown'),
                'vocabulary_usage': writing_patterns.get('vocabulary_usage', 'Unknown'),
                'sentence_structure': writing_patterns.get('sentence_structure', 'Unknown'),
                'text_organization': writing_patterns.get('text_organization', 'Unknown'),
                'flesch_reading_ease': readability.get('flesch_reading_ease', 0.0),
                'gunning_fog': readability.get('gunning_fog', 0.0),
                'vocabulary_richness': lexical.get('vocabulary_richness', 0.0),
                'type_token_ratio': lexical.get('type_token_ratio', 0.0),
                'sentence_complexity': syntactic.get('sentence_complexity', 0.0),
                'syntactic_diversity': syntactic.get('syntactic_diversity', 0.0)
            }
            
            # Save as CSV for easy ML processing
            df = pd.DataFrame([flat_data])
            csv_path = self.output_dir / 'training_data.csv'
            df.to_csv(csv_path, mode='a', header=not csv_path.exists(), index=False)
            
            return str(csv_path)
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return "" 