from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

# Template for database-specific models
# Replace "Template" with your database name (e.g., "OtherDB")

class TemplateDataModel(BaseModel):
    """Template for database-specific data model."""
    id: int
    name: str
    created_at: datetime
    # Add your specific fields here

class TemplateRequestModel(BaseModel):
    """Template for incoming data requests."""
    data: List[Any]
    # Add your specific request fields here

class TemplateResponseModel(BaseModel):
    """Template for API responses."""
    success: bool
    data: List[TemplateDataModel]
    total_count: int 