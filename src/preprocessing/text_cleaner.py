import re
import nltk
from typing import List
import logging

logger = logging.getLogger(__name__)

class TextCleaner:
    """Handles text preprocessing and cleaning operations."""
    
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')
        except Exception as e:
            logger.error(f"Error downloading NLTK data: {str(e)}")
            raise
            
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        
    def clean(self, text: str) -> str:
        """
        Clean and preprocess the input text.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
        
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        return nltk.sent_tokenize(text)
        
    def get_words(self, text: str) -> List[str]:
        """
        Get list of words from text.
        
        Args:
            text: Input text
            
        Returns:
            List of words
        """
        return nltk.word_tokenize(text) 