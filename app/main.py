from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.models import Deal, DealCategory, AISuggestionRequest, AISuggestionResponse, HealthResponse
from app.mock_data import get_all_deals, get_deals_by_category, search_deals_by_keyword

app = FastAPI(
    title="Xmas Gift AI API",
    version="1.0.0",
    description="API REST per suggerimenti regalo personalizzati con mock AI backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", version="1.0.0", ai_backend="mock AI ranking")

@app.get("/")
def root():
    return {"message": "🎄 Xmas Gift AI API", "docs": "/docs"}

@app.get("/deals", response_model=list[Deal])
def get_deals(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    deals = get_all_deals()
    return deals[skip : skip + limit]

@app.get("/deals/category/{category}", response_model=list[Deal])
def get_category(category: DealCategory):
    deals = get_deals_by_category(category)
    if not deals:
        raise HTTPException(status_code=404, detail=f"Nessun prodotto per '{category.value}'")
    return deals

@app.get("/deals/search")
def search(q: str = Query(..., min_length=1)):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query vuota")
    deals = search_deals_by_keyword(q)
    return {"query": q, "total_results": len(deals), "deals": deals}

@app.post("/deals/ai-suggest", response_model=AISuggestionResponse)
def ai_suggest(request: AISuggestionRequest):
    if request.max_results < 1 or request.max_results > 25:
        raise HTTPException(status_code=400, detail="max_results 1-25")
    if request.budget_min > request.budget_max:
        raise HTTPException(status_code=400, detail="budget_min > budget_max")

    all_deals = get_all_deals()
    budget_filtered = [d for d in all_deals if request.budget_min <= float(d.price) <= request.budget_max]

    recipient_lower = request.recipient_description.lower()
    keyword_map = {
        "dinosauri": {"toys": 10}, "gioco": {"toys": 9}, "bambino": {"toys": 9}, "giocattolo": {"toys": 10},
        "puzzle": {"toys": 9}, "costruzioni": {"toys": 10}, "robot": {"toys": 9},
        "gaming": {"electronics": 10}, "tech": {"electronics": 10}, "cuffie": {"electronics": 10},
        "computer": {"electronics": 9}, "smartwatch": {"electronics": 9},
        "moda": {"fashion": 10}, "scarpe": {"fashion": 10}, "sneakers": {"fashion": 10},
        "giacca": {"fashion": 10}, "zaino": {"fashion": 9},
        "crema": {"beauty": 10}, "skincare": {"beauty": 10}, "makeup": {"beauty": 10},
        "trucco": {"beauty": 10}, "viso": {"beauty": 9},
        "casa": {"home": 10}, "lampada": {"home": 8}, "robot": {"home": 9},
    }

    scored_deals = []
    for deal in budget_filtered:
        score = 0
        for keyword, cats in keyword_map.items():
            if keyword in recipient_lower and deal.category.value in cats:
                score += cats[deal.category.value]
        deal_text = (deal.title + " " + deal.description).lower()
        for word in recipient_lower.split():
            if len(word) > 3 and word in deal_text:
                score += 2
        if score > 0:
            scored_deals.append((deal, score))

    scored_deals.sort(key=lambda x: x[1], reverse=True)
    suggested = [deal for deal, _ in scored_deals[:request.max_results]]

    return AISuggestionResponse(
        recipient_description=request.recipient_description,
        suggested_deals=suggested,
        reasoning=f"AI ranking per '{request.recipient_description}' (€{request.budget_min}-{request.budget_max})"
    )
