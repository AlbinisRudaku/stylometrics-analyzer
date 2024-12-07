from typing import Dict, List
import re
import numpy as np
import logging
from collections import Counter

logger = logging.getLogger(__name__)

class StructuralFeatureExtractor:
    """Extracts structural features from text for stylometric analysis."""
    
    def __init__(self):
        self.paragraph_pattern = re.compile(r'\n\s*\n')
        self.sentence_end_pattern = re.compile(r'[.!?]+')
        
    def extract_features(self, text: str) -> Dict[str, float]:
        """
        Extract structural features from the text.
        
        Features include:
        - Paragraph statistics
        - Text organization metrics
        - Whitespace usage
        - Document structure patterns
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary of structural features
        """
        try:
            paragraphs = self.paragraph_pattern.split(text.strip())
            sentences = self.sentence_end_pattern.split(text)
            
            features = {
                # Paragraph metrics
                'avg_paragraph_length': self._calculate_avg_paragraph_length(paragraphs),
                'paragraph_length_variance': self._calculate_paragraph_variance(paragraphs),
                'paragraph_count': len(paragraphs),
                
                # Text organization
                'text_density': self._calculate_text_density(text),
                'whitespace_ratio': self._calculate_whitespace_ratio(text),
                'line_break_frequency': self._calculate_line_break_frequency(text),
                
                # Sentence structure
                'sentence_length_variance': self._calculate_sentence_variance(sentences),
                'avg_sentences_per_paragraph': len(sentences) / len(paragraphs) if paragraphs else 0,
                
                # Document structure
                'structure_consistency': self._calculate_structure_consistency(paragraphs)
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting structural features: {str(e)}")
            raise
            
    def _calculate_avg_paragraph_length(self, paragraphs: List[str]) -> float:
        """Calculate average paragraph length in characters."""
        if not paragraphs:
            return 0
        return np.mean([len(p) for p in paragraphs])
        
    def _calculate_paragraph_variance(self, paragraphs: List[str]) -> float:
        """Calculate variance in paragraph lengths."""
        if not paragraphs:
            return 0
        lengths = [len(p) for p in paragraphs]
        return np.var(lengths)
        
    def _calculate_text_density(self, text: str) -> float:
        """Calculate ratio of non-whitespace characters to total length."""
        if not text:
            return 0
        non_whitespace = len(re.sub(r'\s', '', text))
        return non_whitespace / len(text)
        
    def _calculate_whitespace_ratio(self, text: str) -> float:
        """Calculate ratio of whitespace to text."""
        if not text:
            return 0
        whitespace_count = sum(1 for char in text if char.isspace())
        return whitespace_count / len(text)
        
    def _calculate_line_break_frequency(self, text: str) -> float:
        """Calculate frequency of line breaks."""
        if not text:
            return 0
        line_breaks = text.count('\n')
        return line_breaks / len(text)
        
    def _calculate_sentence_variance(self, sentences: List[str]) -> float:
        """Calculate variance in sentence lengths."""
        if not sentences:
            return 0
        lengths = [len(s.strip()) for s in sentences if s.strip()]
        return np.var(lengths) if lengths else 0
        
    def _calculate_structure_consistency(self, paragraphs: List[str]) -> float:
        """Calculate consistency of paragraph structures."""
        if not paragraphs:
            return 0
        
        # Calculate similarity in paragraph lengths
        lengths = [len(p) for p in paragraphs]
        mean_length = np.mean(lengths)
        std_dev = np.std(lengths)
        
        # Return inverse of coefficient of variation (normalized standard deviation)
        return 1 / (std_dev / mean_length) if mean_length and std_dev else 0 