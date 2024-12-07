from pathlib import Path
from typing import Dict, Any, Union
from src.utils.data_exporter import DataExporter
from src.preprocessing.pdf_extractor import PDFExtractor
from src.preprocessing.text_cleaner import TextCleaner
from src.features.lexical_features import LexicalFeatureExtractor
from src.features.syntactic_features import SyntacticFeatureExtractor
from src.features.structural_features import StructuralFeatureExtractor
from src.features.readability_features import ReadabilityAnalyzer
from src.models.stylometric_model import StylometricAnalyzer
from src.utils.json_formatter import JSONFormatter
from src.utils.data_formatter import DataFormatter
import json
from datetime import datetime
import logging
from tqdm import tqdm
from rich.console import Console

logger = logging.getLogger(__name__)

class StylometricAnalysisApp:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.text_cleaner = TextCleaner()
        self.lexical_extractor = LexicalFeatureExtractor()
        self.syntactic_extractor = SyntacticFeatureExtractor()
        self.structural_extractor = StructuralFeatureExtractor()
        self.readability_analyzer = ReadabilityAnalyzer()
        self.stylometric_analyzer = StylometricAnalyzer()
        self.json_formatter = JSONFormatter()
        self.console = Console()
        self.data_formatter = DataFormatter()

    def analyze_document(self, pdf_path: str, output_format: str = 'dict', output_path: str = None) -> Union[Dict[str, Any], str]:
        try:
            with self.console.status("[bold green]Analyzing document...") as status:
                # Extract text from PDF
                status.update("[bold blue]Extracting text...")
                raw_text = self.pdf_extractor.extract_text(pdf_path)
                status.update("[bold green]Text extracted successfully")
                
                # Get document info
                doc_info = {
                    "filename": Path(pdf_path).name,
                    "file_size": Path(pdf_path).stat().st_size,
                    "page_count": len(self.pdf_extractor.get_pages()) if hasattr(self.pdf_extractor, 'get_pages') else 1
                }
                status.update("[bold blue]Document info collected")
                
                # Clean and preprocess text
                cleaned_text = self.text_cleaner.clean(raw_text)
                status.update("[bold green]Text cleaned")
                
                # Extract features with error handling
                try:
                    lexical_features = self.lexical_extractor.extract_features(cleaned_text)
                    status.update("[bold green]Lexical features extracted")
                except Exception as e:
                    logger.error(f"Error extracting lexical features: {str(e)}")
                    lexical_features = {"vocabulary_richness": 0.0, "type_token_ratio": 0.0}
                
                try:
                    syntactic_features = self.syntactic_extractor.extract_features(cleaned_text)
                    status.update("[bold green]Syntactic features extracted")
                except Exception as e:
                    logger.error(f"Error extracting syntactic features: {str(e)}")
                    syntactic_features = {"sentence_complexity": 0.0, "syntactic_diversity": 0.0}
                
                try:
                    structural_features = self.structural_extractor.extract_features(cleaned_text)
                    status.update("[bold green]Structural features extracted")
                except Exception as e:
                    logger.error(f"Error extracting structural features: {str(e)}")
                    structural_features = {"structure_consistency": 0.0}
                
                try:
                    readability_metrics = self.readability_analyzer.analyze(cleaned_text)
                    status.update("[bold green]Readability metrics calculated")
                except Exception as e:
                    logger.error(f"Error calculating readability metrics: {str(e)}")
                    readability_metrics = {"flesch_reading_ease": 0.0, "gunning_fog": 0.0}
                
                # Perform stylometric analysis
                try:
                    stylometric_results = self.stylometric_analyzer.analyze(
                        lexical_features,
                        syntactic_features,
                        structural_features,
                        readability_metrics
                    )
                    status.update("[bold green]Stylometric analysis completed")
                except Exception as e:
                    logger.error(f"Error in stylometric analysis: {str(e)}")
                    raise  # Re-raise to be caught by outer try-except
                
                # Combine all results
                results = {
                    'metadata': {
                        'filename': doc_info['filename'],
                        'file_size': doc_info['file_size'],
                        'page_count': doc_info['page_count'],
                        'timestamp': datetime.now().isoformat()
                    },
                    'analysis': stylometric_results['analysis'],
                    'features': {
                        'lexical': lexical_features,
                        'syntactic': syntactic_features,
                        'structural': structural_features,
                        'readability': readability_metrics
                    }
                }
                
                # Handle different output formats
                if output_format == 'csv' and output_path:
                    self.data_formatter.to_csv(results, output_path)
                    return f"Results saved to CSV: {output_path}"
                elif output_format == 'ml_json' and output_path:
                    self.data_formatter.to_ml_json(results, output_path)
                    return f"Results saved to ML-friendly JSON: {output_path}"
                elif output_format == 'json':
                    return json.dumps(results)
                elif output_format == 'pretty_json':
                    return json.dumps(results, indent=2)
                return results
                
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            error_result = {
                "metadata": {
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "filename": Path(pdf_path).name if pdf_path else "unknown"
                },
                "analysis": {
                    "style_metrics": {
                        "complexity": {"score": 0.0, "level": "Unknown"},
                        "consistency": {"score": 0.0, "level": "Unknown"},
                        "classification": "Unknown"
                    },
                    "writing_patterns": {
                        "vocabulary_usage": "Unknown",
                        "sentence_structure": "Unknown",
                        "text_organization": "Unknown"
                    }
                },
                "features": {
                    "lexical": {},
                    "syntactic": {},
                    "structural": {},
                    "readability": {}
                }
            }
            
            if output_format == 'json':
                return json.dumps(error_result)
            elif output_format == 'pretty_json':
                return json.dumps(error_result, indent=2)
            return error_result

    def analyze_and_predict(self, pdf_path: str) -> Dict[str, Any]:
        # Get basic analysis
        analysis_results = self.analyze_document(pdf_path)
        
        # Export for training
        self.data_exporter.export_for_training(analysis_results, Path(pdf_path).name)
        
        try:
            # Get AI predictions
            predictions = self.prediction_service.predict_style(analysis_results)
            # Combine results
            analysis_results['predictions'] = predictions.dict()
        except Exception as e:
            # If predictions fail, continue without them
            analysis_results['predictions'] = {
                'style_classification': analysis_results['analysis']['style_metrics']['classification'],
                'confidence_score': 1.0,
                'writing_patterns': analysis_results['analysis']['writing_patterns'],
                'recommendations': analysis_results['summary']['recommendations']
            }
        
        # Visualize results
        self.dashboard.visualize_analysis(analysis_results)
        
        return analysis_results

    async def analyze_document_async(self, pdf_path: str):
        """Async version of document analysis"""
        # Async implementation