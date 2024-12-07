import numpy as np
from typing import Dict, List, Any
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd

logger = logging.getLogger(__name__)

class StylometricAnalyzer:
    """Analyzes stylometric features to identify writing patterns and style characteristics."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=1)
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        
    def analyze(
        self,
        lexical_features: Dict[str, float],
        syntactic_features: Dict[str, float],
        structural_features: Dict[str, float],
        readability_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze stylometric features and return structured results."""
        try:
            # Calculate complexity score (0-1)
            complexity_score = (
                lexical_features.get('vocabulary_richness', 0) * 0.4 +
                syntactic_features.get('sentence_complexity', 0) * 0.4 +
                readability_metrics.get('gunning_fog', 0) / 20 * 0.2  # Normalize Gunning Fog
            )
            
            # Calculate consistency score (0-1)
            consistency_score = structural_features.get('structure_consistency', 0)
            
            # Determine complexity level
            complexity_level = self._get_level(complexity_score)
            consistency_level = self._get_level(consistency_score)
            
            # Determine writing style classification
            classification = self._classify_style(complexity_score, consistency_score)
            
            # Calculate additional metrics
            readability_score = self._calculate_readability_score(readability_metrics)
            vocabulary_score = self._calculate_vocabulary_score(lexical_features)
            structure_score = self._calculate_structure_score(structural_features, syntactic_features)
            
            return {
                'analysis': {
                    'style_metrics': {
                        'complexity': {
                            'score': round(complexity_score, 2),
                            'level': complexity_level,
                            'components': {
                                'vocabulary_contribution': round(lexical_features.get('vocabulary_richness', 0) * 0.4, 2),
                                'syntax_contribution': round(syntactic_features.get('sentence_complexity', 0) * 0.4, 2),
                                'readability_contribution': round(readability_metrics.get('gunning_fog', 0) / 20 * 0.2, 2)
                            }
                        },
                        'consistency': {
                            'score': round(consistency_score, 2),
                            'level': consistency_level
                        },
                        'classification': classification
                    },
                    'writing_patterns': {
                        'vocabulary_usage': self._analyze_vocabulary(lexical_features),
                        'sentence_structure': self._analyze_sentences(syntactic_features),
                        'text_organization': self._analyze_organization(structural_features)
                    },
                    'summary_metrics': {
                        'readability': {
                            'score': round(readability_score, 2),
                            'interpretation': self._interpret_readability(readability_score)
                        },
                        'vocabulary': {
                            'score': round(vocabulary_score, 2),
                            'interpretation': self._interpret_vocabulary(vocabulary_score)
                        },
                        'structure': {
                            'score': round(structure_score, 2),
                            'interpretation': self._interpret_structure(structure_score)
                        }
                    },
                    'recommendations': self._generate_recommendations(
                        readability_score,
                        vocabulary_score,
                        structure_score,
                        complexity_score,
                        consistency_score
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Error in stylometric analysis: {str(e)}")
            return self._generate_error_response()

    def _get_level(self, score: float) -> str:
        if score < 0.3: return "Low"
        if score < 0.7: return "Medium"
        return "High"

    def _classify_style(self, complexity: float, consistency: float) -> str:
        if complexity > 0.7 and consistency > 0.7:
            return "Academic"
        if complexity < 0.3 and consistency > 0.7:
            return "Simple and Structured"
        if complexity > 0.7 and consistency < 0.3:
            return "Complex and Variable"
        return "Balanced"
        
    def _analyze_vocabulary(self, lexical_features: Dict[str, float]) -> str:
        """Categorize vocabulary usage patterns."""
        richness = lexical_features.get('vocabulary_richness', 0)
        if richness > 0.7: return "Advanced"
        if richness > 0.3: return "Moderate"
        return "Basic"
        
    def _analyze_sentences(self, syntactic_features: Dict[str, float]) -> str:
        """Categorize sentence structure patterns."""
        complexity = syntactic_features.get('sentence_complexity', 0)
        if complexity > 0.7: return "Complex"
        if complexity > 0.3: return "Varied"
        return "Simple"
        
    def _analyze_organization(self, structural_features: Dict[str, float]) -> str:
        """Categorize text organization patterns."""
        consistency = structural_features.get('structure_consistency', 0)
        if consistency > 0.7: return "Well Structured"
        if consistency > 0.3: return "Moderately Structured"
        return "Loosely Structured"

    def _calculate_readability_score(self, metrics: Dict[str, float]) -> float:
        """Calculate normalized readability score."""
        flesch = metrics.get('flesch_reading_ease', 0)
        fog = metrics.get('gunning_fog', 0)
        # Normalize Flesch score (0-100) to 0-1
        norm_flesch = max(0, min(flesch, 100)) / 100
        # Normalize Gunning Fog (6-20) to 0-1
        norm_fog = max(0, min(20 - fog, 14)) / 14
        return (norm_flesch + norm_fog) / 2

    def _calculate_vocabulary_score(self, features: Dict[str, float]) -> float:
        """Calculate vocabulary richness score."""
        richness = features.get('vocabulary_richness', 0)
        diversity = features.get('type_token_ratio', 0)
        return (richness + diversity) / 2

    def _calculate_structure_score(self, structural: Dict[str, float], syntactic: Dict[str, float]) -> float:
        """Calculate overall structure score."""
        consistency = structural.get('structure_consistency', 0)
        complexity = syntactic.get('sentence_complexity', 0) / 100  # Normalize
        return (consistency + (1 - complexity)) / 2

    def _interpret_readability(self, score: float) -> str:
        if score > 0.8: return "Very Easy to Read"
        if score > 0.6: return "Easy to Read"
        if score > 0.4: return "Moderately Readable"
        if score > 0.2: return "Difficult to Read"
        return "Very Difficult to Read"

    def _interpret_vocabulary(self, score: float) -> str:
        if score > 0.8: return "Advanced and Diverse"
        if score > 0.6: return "Sophisticated"
        if score > 0.4: return "Balanced"
        if score > 0.2: return "Basic"
        return "Limited"

    def _interpret_structure(self, score: float) -> str:
        if score > 0.8: return "Well Structured and Balanced"
        if score > 0.6: return "Clear and Organized"
        if score > 0.4: return "Moderately Structured"
        if score > 0.2: return "Somewhat Disorganized"
        return "Poorly Structured"

    def _generate_recommendations(self, readability: float, vocabulary: float, 
                                structure: float, complexity: float, consistency: float) -> List[str]:
        """Generate specific recommendations based on scores."""
        recommendations = []
        
        if readability < 0.4:
            recommendations.append("Consider simplifying sentence structure for better readability")
        if vocabulary < 0.4:
            recommendations.append("Try incorporating more varied vocabulary while maintaining clarity")
        if structure < 0.4:
            recommendations.append("Work on organizing content with clearer paragraph structure")
        if complexity > 0.8:
            recommendations.append("Consider breaking down complex ideas into simpler components")
        if consistency < 0.3:
            recommendations.append("Try to maintain more consistent paragraph lengths and structure")
            
        if not recommendations:
            recommendations.append("Your writing demonstrates good balance across all metrics")
            
        return recommendations

    def _generate_error_response(self) -> Dict[str, Any]:
        """Generate error response."""
        return {
            'analysis': {
                'style_metrics': {
                    'complexity': {
                        'score': 0.0,
                        'level': 'Unknown'
                    },
                    'consistency': {
                        'score': 0.0,
                        'level': 'Unknown'
                    },
                    'classification': 'Unknown'
                },
                'writing_patterns': {
                    'vocabulary_usage': 'Unknown',
                    'sentence_structure': 'Unknown',
                    'text_organization': 'Unknown'
                },
                'summary_metrics': {
                    'readability': {
                        'score': 0.0,
                        'interpretation': 'Unknown'
                    },
                    'vocabulary': {
                        'score': 0.0,
                        'interpretation': 'Unknown'
                    },
                    'structure': {
                        'score': 0.0,
                        'interpretation': 'Unknown'
                    }
                },
                'recommendations': ['An error occurred during analysis']
            }
        } 