from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from decimal import Decimal


class DealCategory(str, Enum):
    electronics = "electronics"
    beauty = "beauty"
    home = "home"
    toys = "toys"
    fashion = "fashion"


class Deal(BaseModel):
    id: int = Field(..., gt=0, description="ID univoco del prodotto")
    title: str = Field(..., min_length=1, max_length=100, description="Titolo del prodotto")
    description: str = Field(..., min_length=10, max_length=500, description="Descrizione dettagliata")
    price: Decimal = Field(..., gt=0, le=5000, description="Prezzo scontato in €")
    original_price: Decimal = Field(..., gt=0, le=10000, description="Prezzo originale in €")
    discount: int = Field(..., ge=0, le=100, description="Percentuale sconto (0-100%)")
    category: DealCategory = Field(..., description="Categoria del prodotto")
    image_url: str = Field(..., min_length=1, description="URL immagine placeholder")
    url: str = Field(..., min_length=1, description="URL del deal")

    class Config:
        json_encoders = {Decimal: float}
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Cuffie Wireless Premium",
                "description": "Cuffie over-ear noise cancelling con batteria 40h",
                "price": 89.99,
                "original_price": 179.99,
                "discount": 50,
                "category": "electronics",
                "image_url": "https://example.com/headphones.jpg",
                "url": "https://example.com/deal/1"
            }
        }

    @validator('price')
    def price_must_be_less_original(cls, v, values):
        if 'original_price' in values and v > values['original_price']:
            raise ValueError('price deve essere minore o uguale a original_price')
        return v

    @validator('discount')
    def discount_must_be_coherent(cls, v, values):
        if 'price' in values and 'original_price' in values:
            expected_discount = int(100 * (1 - values['price'] / values['original_price']))
            if abs(v - expected_discount) > 1:
                raise ValueError(f"Discount {v}% non corrisponde ai prezzi ({expected_discount}% atteso)")
        return v


class AISuggestionRequest(BaseModel):
    recipient_description: str = Field(..., min_length=5, max_length=500, description="Descrizione del destinatario")
    budget_min: Optional[Decimal] = Field(0, gt=-1, le=5000, description="Budget minimo in €")
    budget_max: Optional[Decimal] = Field(1000, gt=0, le=10000, description="Budget massimo in €")
    max_results: int = Field(5, ge=1, le=25, description="Numero massimo di suggerimenti")

    class Config:
        json_encoders = {Decimal: float}
        schema_extra = {
            "example": {
                "recipient_description": "donna 30 anni appassionata di tech e skincare",
                "budget_min": 20,
                "budget_max": 150,
                "max_results": 5
            }
        }


class AISuggestionResponse(BaseModel):
    recipient_description: str
    suggested_deals: List[Deal]
    reasoning: str = Field(..., min_length=1, description="Motivazione dei suggerimenti")

    class Config:
        json_encoders = {Decimal: float}
        schema_extra = {
            "example": {
                "recipient_description": "donna 30 anni appassionata di tech",
                "reasoning": "Suggerimenti basati su budget €20-€150",
                "suggested_deals": []
            }
        }


class HealthResponse(BaseModel):
    status: str
    version: str
    ai_backend: str

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "ai_backend": "ollama mock"
            }
        }
