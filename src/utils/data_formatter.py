import pandas as pd
from typing import Dict, Any, List
import json
from pathlib import Path

class DataFormatter:
    """Handles formatting of analysis results for different output formats"""
    
    @staticmethod
    def _flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV format"""
        items: List = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataFormatter._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists by joining elements with semicolons
                items.append((new_key, ';'.join(map(str, v))))
            else:
                items.append((new_key, v))
        return dict(items)

    def to_csv(self, data: Dict[str, Any], output_path: str) -> None:
        """Convert analysis results to CSV format"""
        # Extract key metrics for ML training
        ml_features = {
            'document_id': data['metadata']['filename'],
            'timestamp': data['metadata']['timestamp'],
            'file_size': data['metadata']['file_size'],
            'complexity_score': data['analysis']['style_metrics']['complexity']['score'],
            'consistency_score': data['analysis']['style_metrics']['consistency']['score'],
            'classification': data['analysis']['style_metrics']['classification'],
            'vocabulary_usage': data['analysis']['writing_patterns']['vocabulary_usage'],
            'sentence_structure': data['analysis']['writing_patterns']['sentence_structure'],
            'text_organization': data['analysis']['writing_patterns']['text_organization'],
            # Lexical features
            'avg_word_length': data['features']['lexical']['avg_word_length'],
            'vocabulary_richness': data['features']['lexical']['vocabulary_richness'],
            'type_token_ratio': data['features']['lexical']['type_token_ratio'],
            # Syntactic features
            'avg_sentence_length': data['features']['syntactic']['avg_sentence_length'],
            'sentence_complexity': data['features']['syntactic']['sentence_complexity'],
            'syntactic_diversity': data['features']['syntactic']['syntactic_diversity'],
            # Structural features
            'avg_paragraph_length': data['features']['structural']['avg_paragraph_length'],
            'text_density': data['features']['structural']['text_density'],
            'structure_consistency': data['features']['structural']['structure_consistency'],
            # Readability features
            'flesch_reading_ease': data['features']['readability']['flesch_reading_ease'],
            'gunning_fog': data['features']['readability']['gunning_fog'],
            'flesch_kincaid_grade': data['features']['readability']['flesch_kincaid_grade']
        }
        
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame([ml_features])
        df.to_csv(output_path, index=False)
        
    def to_ml_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert analysis results to ML-friendly JSON format"""
        return {
            'document_id': data['metadata']['filename'],
            'timestamp': data['metadata']['timestamp'],
            'features': {
                'lexical': {
                    'vocabulary_richness': data['features']['lexical']['vocabulary_richness'],
                    'type_token_ratio': data['features']['lexical']['type_token_ratio'],
                    'avg_word_length': data['features']['lexical']['avg_word_length'],
                    'hapax_ratio': data['features']['lexical']['hapax_ratio']
                },
                'syntactic': {
                    'sentence_complexity': data['features']['syntactic']['sentence_complexity'],
                    'avg_sentence_length': data['features']['syntactic']['avg_sentence_length'],
                    'syntactic_diversity': data['features']['syntactic']['syntactic_diversity']
                },
                'structural': {
                    'avg_paragraph_length': data['features']['structural']['avg_paragraph_length'],
                    'structure_consistency': data['features']['structural']['structure_consistency']
                },
                'readability': {
                    'flesch_reading_ease': data['features']['readability']['flesch_reading_ease'],
                    'gunning_fog': data['features']['readability']['gunning_fog']
                }
            },
            'metrics': {
                'complexity': data['analysis']['style_metrics']['complexity']['score'],
                'consistency': data['analysis']['style_metrics']['consistency']['score']
            },
            'classifications': {
                'style': data['analysis']['style_metrics']['classification'],
                'vocabulary_usage': data['analysis']['writing_patterns']['vocabulary_usage'],
                'sentence_structure': data['analysis']['writing_patterns']['sentence_structure']
            }
        } 