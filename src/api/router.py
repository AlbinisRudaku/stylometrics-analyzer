from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel
import tempfile
import os
import shutil
from src.stylometric_analysis_app import StylometricAnalysisApp
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter()

class AnalysisResponse(BaseModel):
    """Analysis response schema"""
    metadata: dict
    analysis: dict
    features: dict

@router.post("/analyze", 
    response_model=AnalysisResponse,
    dependencies=[Depends(RateLimiter(times=10, minutes=1))])  # 10 requests per minute
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

@router.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@router.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred"}
    )