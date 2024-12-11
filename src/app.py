from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import router
import os

app = FastAPI(
    title="Stilo API",
    description="Stylometric Analysis API",
    version="1.0.0"
)

# Configure CORS with environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api")

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}