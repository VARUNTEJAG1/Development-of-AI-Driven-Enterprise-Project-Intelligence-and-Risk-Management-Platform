from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import os
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Project Risk Forecasting System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./project_risk.db"
    
    # ML Models
    MODEL_PATH: str = "ml_models/risk_model.joblib"
    METADATA_PATH: str = "ml_models/model_metadata.json"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8501",
        "*"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # Fallback if invalid JSON (like single quotes)
                    v = v.strip("[]")
            return [origin.strip().strip("'\"") for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
