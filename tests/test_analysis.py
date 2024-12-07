import pytest
from src.stylometric_analysis_app import StylometricAnalysisApp

@pytest.fixture
def analysis_app():
    return StylometricAnalysisApp()

def test_analyze_document(analysis_app, test_pdf):
    results = analysis_app.analyze_document(test_pdf)
    assert 'metadata' in results
    assert 'analysis' in results
    assert 'features' in results 