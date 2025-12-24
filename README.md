# 🎄 Xmas Gift AI API

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/xmas-gift-ai-api/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/xmas-gift-ai-api/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un'API FastAPI intelligente che aggrega offerte natalizie e le categorizza utilizzando **AI** (Ollama locale o HuggingFace Inference API). 🤖✨

## ✨ Caratteristiche Principali

### 1. **Data Collection**
- Mock data realistico con 12+ offerte natalizie
- Estrazione: titolo, prezzo, URL, categoria, sconto

### 2. **API REST Completa**
- \GET /deals\ - Tutte le offerte
- \GET /deals/category/{name}\ - Filtro per categoria  
- \POST /deals/ai-suggest\ - **AI Suggerimenti personalizzati**
