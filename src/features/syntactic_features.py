import spacy
from typing import Dict, List, Tuple
import logging
from collections import Counter
import numpy as np

logger = logging.getLogger(__name__)

class SyntacticFeatureExtractor:
    """Extracts syntactic features from text for stylometric analysis."""
    
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            logger.error("Error loading spaCy model. Please run: python -m spacy download en_core_web_sm")
            raise
            
    def extract_features(self, text: str) -> Dict[str, float]:
        """
        Extract syntactic features from the text.
        
        Features include:
        - POS tag distributions
        - Dependency relation patterns
        - Phrase structure patterns
        - Sentence complexity metrics
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary of syntactic features
        """
        try:
            doc = self.nlp(text)
            
            features = {
                # Sentence structure metrics
                'avg_sentence_length': self._calculate_avg_sentence_length(doc),
                'sentence_complexity': self._calculate_sentence_complexity(doc),
                
                # Parse tree metrics
                'avg_parse_tree_depth': self._calculate_parse_tree_depth(doc),
                'parse_tree_breadth': self._calculate_parse_tree_breadth(doc),
                
                # Syntactic diversity
                'syntactic_diversity': self._calculate_syntactic_diversity(doc),
                
                # Clause metrics
                'subordinate_clause_ratio': self._calculate_subordinate_ratio(doc),
                
                # Function word usage
                'function_word_ratio': self._calculate_function_word_ratio(doc)
            }
            
            # Add POS tag distributions
            pos_distributions = self._calculate_pos_distributions(doc)
            features.update(pos_distributions)
            
            # Add dependency relation patterns
            dep_patterns = self._calculate_dependency_patterns(doc)
            features.update(dep_patterns)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting syntactic features: {str(e)}")
            raise
            
    def _calculate_avg_sentence_length(self, doc) -> float:
        """Calculate average sentence length in tokens."""
        sentences = list(doc.sents)
        if not sentences:
            return 0
        return np.mean([len(sent) for sent in sentences])
        
    def _calculate_sentence_complexity(self, doc) -> float:
        """Calculate sentence complexity based on clause structure."""
        if not len(doc):
            return 0
        verb_counts = [len([token for token in sent if token.pos_ == "VERB"]) 
                      for sent in doc.sents]
        return np.mean(verb_counts) if verb_counts else 0
        
    def _calculate_parse_tree_depth(self, doc) -> float:
        """Calculate average depth of parse trees."""
        def get_depth(token):
            return max([get_depth(child) for child in token.children] or [0]) + 1
            
        depths = [get_depth(sent.root) for sent in doc.sents]
        return np.mean(depths) if depths else 0
        
    def _calculate_parse_tree_breadth(self, doc) -> float:
        """Calculate average branching factor of parse trees."""
        breadths = [len(list(sent.root.children)) for sent in doc.sents]
        return np.mean(breadths) if breadths else 0
        
    def _calculate_pos_distributions(self, doc) -> Dict[str, float]:
        """Calculate distribution of POS tags."""
        if not len(doc):
            return {}
            
        pos_counts = Counter(token.pos_ for token in doc)
        total_tokens = len(doc)
        
        return {
            f'pos_{pos.lower()}': count/total_tokens 
            for pos, count in pos_counts.items()
        }
        
    def _calculate_dependency_patterns(self, doc) -> Dict[str, float]:
        """Calculate frequency of dependency relation patterns."""
        if not len(doc):
            return {}
            
        dep_counts = Counter(token.dep_ for token in doc)
        total_deps = len(doc)
        
        return {
            f'dep_{dep.lower()}': count/total_deps 
            for dep, count in dep_counts.items()
        }
        
    def _calculate_syntactic_diversity(self, doc) -> float:
        """Calculate syntactic diversity using unique dependency patterns."""
        if not len(doc):
            return 0
        unique_patterns = set((token.dep_, token.head.pos_) for token in doc)
        return len(unique_patterns) / len(doc)
        
    def _calculate_subordinate_ratio(self, doc) -> float:
        """Calculate ratio of subordinate clauses."""
        if not len(doc):
            return 0
        subordinate_count = sum(1 for token in doc if token.dep_ in {'advcl', 'acl', 'ccomp', 'xcomp'})
        return subordinate_count / len(doc)
        
    def _calculate_function_word_ratio(self, doc) -> float:
        """Calculate ratio of function words to content words."""
        if not len(doc):
            return 0
        function_words = sum(1 for token in doc if token.pos_ in {'ADP', 'AUX', 'CCONJ', 'DET', 'PART', 'PRON', 'SCONJ'})
        return function_words / len(doc) 