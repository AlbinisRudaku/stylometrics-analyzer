import json
from typing import Dict, Any
from datetime import datetime
import numpy as np

class JSONFormatter:
    """Formats stylometric analysis results into a structured JSON format."""
    
    @staticmethod
    def format_results(analysis_results: Dict[str, Any], document_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format analysis results into a structured JSON format.
        
        Args:
            analysis_results: Raw analysis results
            document_info: Information about the analyzed document
            
        Returns:
            Formatted JSON-compatible dictionary
        """
        # Custom JSON encoder to handle numpy types and other special objects
        class NumpyEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                if isinstance(obj, np.float32):
                    return float(obj)
                return super().default(obj)
        
        formatted_results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "document": {
                    "filename": document_info.get("filename", ""),
                    "file_size": document_info.get("file_size", 0),
                    "page_count": document_info.get("page_count", 0)
                },
                "version": "1.0.0"
            },
            "analysis": {
                "style_metrics": {
                    "complexity": {
                        "score": analysis_results["style_complexity"],
                        "level": _get_complexity_level(analysis_results["style_complexity"])
                    },
                    "consistency": {
                        "score": analysis_results["style_consistency"],
                        "level": _get_consistency_level(analysis_results["style_consistency"])
                    },
                    "classification": analysis_results["style_classification"]
                },
                "writing_patterns": analysis_results["writing_patterns"],
                "readability": {
                    metric: value
                    for metric, value in analysis_results.get("readability_metrics", {}).items()
                },
                "lexical_analysis": {
                    metric: value
                    for metric, value in analysis_results.get("lexical_features", {}).items()
                },
                "structural_analysis": {
                    metric: value
                    for metric, value in analysis_results.get("structural_features", {}).items()
                },
                "syntactic_analysis": {
                    metric: value
                    for metric, value in analysis_results.get("syntactic_features", {}).items()
                }
            },
            "summary": {
                "primary_style": analysis_results["style_classification"],
                "key_characteristics": _extract_key_characteristics(analysis_results),
                "recommendations": _generate_recommendations(analysis_results)
            }
        }
        
        # Convert to JSON-compatible format
        return json.loads(json.dumps(formatted_results, cls=NumpyEncoder))

def _get_complexity_level(score: float) -> str:
    """Convert complexity score to descriptive level."""
    if score >= 0.8:
        return "Very High"
    elif score >= 0.6:
        return "High"
    elif score >= 0.4:
        return "Moderate"
    elif score >= 0.2:
        return "Low"
    return "Very Low"

def _get_consistency_level(score: float) -> str:
    """Convert consistency score to descriptive level."""
    if score >= 0.8:
        return "Highly Consistent"
    elif score >= 0.6:
        return "Consistent"
    elif score >= 0.4:
        return "Moderately Consistent"
    elif score >= 0.2:
        return "Inconsistent"
    return "Highly Inconsistent"

def _extract_key_characteristics(results: Dict[str, Any]) -> list:
    """Extract key characteristics from analysis results."""
    characteristics = []
    
    # Add writing pattern characteristics
    patterns = results.get("writing_patterns", {})
    for category, pattern in patterns.items():
        characteristics.append(f"{category.replace('_', ' ').title()}: {pattern}")
    
    return characteristics

def _generate_recommendations(results: Dict[str, Any]) -> list:
    """Generate recommendations based on analysis results."""
    recommendations = []
    
    # Example recommendation logic
    if results.get("style_complexity", 0) < 0.4:
        recommendations.append("Consider incorporating more complex sentence structures")
    if results.get("style_consistency", 0) < 0.4:
        recommendations.append("Work on maintaining consistent paragraph lengths")
    
    return recommendations 