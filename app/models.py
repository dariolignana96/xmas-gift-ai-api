from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal

class DealCategory(str, Enum):
    electronics = "electronics"
    beauty = "beauty"
    home = "home"
    toys = "toys"
    fashion = "fashion"

class Deal(BaseModel):
    model_config = {"json_encoders": {Decimal: float}}
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    price: Decimal = Field(..., gt=0, le=5000)
    original_price: Decimal = Field(..., gt=0, le=10000)
    discount: int = Field(..., ge=0, le=100)
    category: DealCategory
    image_url: str = Field(default="")
    url: str = Field(..., min_length=1)

class AISuggestionRequest(BaseModel):
    recipient_description: str = Field(..., min_length=5, max_length=500)
    budget_min: float = Field(0, gt=-1, le=5000)
    budget_max: float = Field(1000, gt=0, le=10000)
    max_results: int = Field(5, ge=1, le=25)

class AISuggestionResponse(BaseModel):
    recipient_description: str
    suggested_deals: List[Deal]
    reasoning: str = Field(..., min_length=1)

class HealthResponse(BaseModel):
    status: str
    version: str
    ai_backend: str
