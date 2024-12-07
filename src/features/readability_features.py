import logging
import math
from typing import Dict, List
import nltk
from textblob import TextBlob
import re

logger = logging.getLogger(__name__)

class ReadabilityAnalyzer:
    """Analyzes text readability using various metrics."""
    
    def __init__(self):
        self.syllable_dict = {}
        self.sentence_pattern = re.compile(r'[.!?]+(?=\s+|$)')
        
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Calculate various readability metrics.
        
        Implements:
        - Flesch Reading Ease
        - Flesch-Kincaid Grade Level
        - Gunning Fog Index
        - SMOG Index
        - Dale-Chall Score
        - Automated Readability Index
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary of readability metrics
        """
        try:
            # Split text into sentences using regex
            sentences = [s.strip() for s in self.sentence_pattern.split(text) if s.strip()]
            # Split into words (simpler approach)
            words = [w for w in text.split() if w.strip()]
            
            num_sentences = len(sentences)
            num_words = len(words)
            num_syllables = sum(self._count_syllables(word) for word in words)
            num_complex_words = sum(1 for word in words if self._count_syllables(word) >= 3)
            
            metrics = {
                'flesch_reading_ease': self._flesch_reading_ease(
                    num_syllables, num_words, num_sentences
                ),
                'flesch_kincaid_grade': self._flesch_kincaid_grade(
                    num_syllables, num_words, num_sentences
                ),
                'gunning_fog': self._gunning_fog(
                    num_words, num_complex_words, num_sentences
                ),
                'smog_index': self._smog_index(
                    num_complex_words, num_sentences
                ),
                'automated_readability_index': self._automated_readability_index(
                    text, num_words, num_sentences
                ),
                'average_syllables_per_word': num_syllables / num_words if num_words else 0,
                'complex_word_ratio': num_complex_words / num_words if num_words else 0
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating readability metrics: {str(e)}")
            raise
            
    def _count_syllables(self, word: str) -> int:
        """Count the number of syllables in a word."""
        word = word.lower()
        
        # Check cache
        if word in self.syllable_dict:
            return self.syllable_dict[word]
            
        # Count vowel groups
        count = 0
        vowels = "aeiouy"
        prev_char_is_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_is_vowel:
                count += 1
            prev_char_is_vowel = is_vowel
            
        # Adjust for silent e
        if word.endswith('e'):
            count -= 1
            
        # Ensure at least one syllable
        count = max(1, count)
        
        # Cache result
        self.syllable_dict[word] = count
        return count
        
    def _flesch_reading_ease(self, syllables: int, words: int, sentences: int) -> float:
        """Calculate Flesch Reading Ease score."""
        if not words or not sentences:
            return 0
        return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        
    def _flesch_kincaid_grade(self, syllables: int, words: int, sentences: int) -> float:
        """Calculate Flesch-Kincaid Grade Level."""
        if not words or not sentences:
            return 0
        return 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        
    def _gunning_fog(self, words: int, complex_words: int, sentences: int) -> float:
        """Calculate Gunning Fog Index."""
        if not words or not sentences:
            return 0
        return 0.4 * ((words / sentences) + 100 * (complex_words / words))
        
    def _smog_index(self, complex_words: int, sentences: int) -> float:
        """Calculate SMOG Index."""
        if not sentences:
            return 0
        return 1.0430 * math.sqrt(complex_words * (30 / sentences)) + 3.1291
        
    def _automated_readability_index(self, text: str, words: int, sentences: int) -> float:
        """Calculate Automated Readability Index."""
        if not words or not sentences:
            return 0
        characters = len(text) - text.count(' ')
        return 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43 