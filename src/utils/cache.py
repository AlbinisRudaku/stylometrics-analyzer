from functools import lru_cache
from pathlib import Path

class AnalysisCache:
    @lru_cache(maxsize=100)
    def get_document_analysis(self, file_path: str, file_hash: str):
        """Cache analysis results based on file path and hash"""
        pass 