import numpy as np
from typing import Dict, List
import re
from collections import Counter
import logging
from textblob import TextBlob

logger = logging.getLogger(__name__)

class LexicalFeatureExtractor:
    """Extracts lexical features from text for stylometric analysis."""
    
    def __init__(self):
        self.word_pattern = re.compile(r'\b\w+\b')
        
    def extract_features(self, text: str) -> Dict[str, float]:
        """
        Extract lexical features from the text.
        
        Features include:
        - Average word length
        - Vocabulary richness
        - Type-Token Ratio (TTR)
        - Hapax Legomena ratio
        - Character frequency distributions
        - Word length distributions
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary of lexical features
        """
        try:
            # Basic text statistics
            words = self.word_pattern.findall(text.lower())
            word_counts = Counter(words)
            char_counts = Counter(text)
            
            # Calculate features
            features = {
                'avg_word_length': self._calculate_avg_word_length(words),
                'vocabulary_richness': len(word_counts) / len(words) if words else 0,
                'type_token_ratio': self._calculate_ttr(words),
                'hapax_ratio': self._calculate_hapax_ratio(word_counts, len(words)),
                'char_diversity': len(char_counts) / len(text) if text else 0,
                'word_length_variance': self._calculate_word_length_variance(words),
                'unique_words_ratio': len(set(words)) / len(words) if words else 0,
                'punctuation_ratio': self._calculate_punctuation_ratio(text)
            }
            
            # Add character frequency distributions
            char_freqs = self._calculate_char_frequencies(text)
            features.update(char_freqs)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting lexical features: {str(e)}")
            raise
            
    def _calculate_avg_word_length(self, words: List[str]) -> float:
        """Calculate average word length."""
        if not words:
            return 0
        return np.mean([len(word) for word in words])
        
    def _calculate_ttr(self, words: List[str]) -> float:
        """Calculate Type-Token Ratio."""
        if not words:
            return 0
        return len(set(words)) / len(words)
        
    def _calculate_hapax_ratio(self, word_counts: Counter, total_words: int) -> float:
        """Calculate ratio of words that appear only once."""
        if not total_words:
            return 0
        hapax_count = sum(1 for count in word_counts.values() if count == 1)
        return hapax_count / total_words
        
    def _calculate_word_length_variance(self, words: List[str]) -> float:
        """Calculate variance in word lengths."""
        if not words:
            return 0
        word_lengths = [len(word) for word in words]
        return np.var(word_lengths)
        
    def _calculate_char_frequencies(self, text: str) -> Dict[str, float]:
        """Calculate character frequency distributions."""
        if not text:
            return {}
            
        char_counts = Counter(text.lower())
        total_chars = len(text)
        
        return {
            f'freq_{char}': count/total_chars 
            for char, count in char_counts.items()
            if char.isalpha()
        }
        
    def _calculate_punctuation_ratio(self, text: str) -> float:
        """Calculate ratio of punctuation marks to total characters."""
        if not text:
            return 0
        punctuation_count = sum(1 for char in text if not char.isalnum() and not char.isspace())
        return punctuation_count / len(text) 