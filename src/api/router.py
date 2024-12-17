from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import tempfile
import os
import shutil
from src.stylometric_analysis_app import StylometricAnalysisApp
from fastapi.responses import JSONResponse

router = APIRouter()

class AnalysisResponse(BaseModel):
    """Analysis response schema"""
    metadata: dict
    analysis: dict
    features: dict

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze a document for stylometric features
    
    Args:
        file: PDF file to analyze
        
    Returns:
        AnalysisResponse: Complete analysis results
        
    Raises:
        HTTPException: If file processing fails
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    try:
        # Create a temporary directory that will be automatically cleaned up
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Create temporary file path
                temp_path = os.path.join(temp_dir, file.filename)
                
                # Save uploaded file
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Process the document
                analyzer = StylometricAnalysisApp()
                results = analyzer.analyze_document(temp_path)
                
                return results
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing document: {str(e)}"
                )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))