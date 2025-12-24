from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.models import Deal, DealCategory, AISuggestionRequest, AISuggestionResponse, HealthResponse
from app.mock_data import get_all_deals, get_deals_by_category, search_deals_by_keyword


app = FastAPI(
    title="Xmas Gift AI API",
    version="1.0.0",
    description="API REST per suggerimenti regalo personalizzati con mock AI backend"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint.
    Verifica che il backend sia online e operativo.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ai_backend="ollama mock",
    )


@app.get("/")
def root():
    """
    Root endpoint con benvenuto e link alla documentazione.
    """
    return {
        "message": "🎄 Xmas Gift AI API - 100% Open Source",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/deals", response_model=list[Deal])
def get_deals(
    skip: int = Query(0, ge=0, description="Numero di prodotti da saltare"),
    limit: int = Query(10, ge=1, le=100, description="Numero massimo di prodotti da restituire"),
):
    """
    Restituisce la lista paginata di tutti i prodotti.
    """
    deals = get_all_deals()
    return deals[skip : skip + limit]


@app.get("/deals/category/{category}", response_model=list[Deal])
def get_category(category: DealCategory):
    """
    Restituisce tutti i prodotti di una categoria specifica.
    """
    deals = get_deals_by_category(category)

    if not deals:
        raise HTTPException(
            status_code=404,
            detail=f"Nessun prodotto trovato per la categoria '{category.value}'",
        )

    return deals


@app.get("/deals/search")
def search(q: str = Query(..., min_length=1, description="Parola chiave di ricerca")):
    """
    Ricerca prodotti per parola chiave (titolo e descrizione).
    """
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Il parametro di ricerca non può essere vuoto",
        )

    deals = search_deals_by_keyword(q)

    return {
        "query": q,
        "total_results": len(deals),
        "deals": deals,
    }


@app.post("/deals/ai-suggest", response_model=AISuggestionResponse)
def ai_suggest(request: AISuggestionRequest):
    """
    Ottiene suggerimenti regalo personalizzati basati su descrizione e budget.
    Utilizza algoritmo di ranking basato su keyword matching della descrizione recipient.
    """
    if request.max_results < 1 or request.max_results > 25:
        raise HTTPException(
            status_code=400,
            detail="max_results deve essere tra 1 e 25",
        )

    if request.budget_min < 0 or request.budget_max < 0:
        raise HTTPException(
            status_code=400,
            detail="Budget non può essere negativo",
        )

    if request.budget_min > request.budget_max:
        raise HTTPException(
            status_code=400,
            detail="budget_min non può essere maggiore di budget_max",
        )

    # Step 1: Filtra per budget
    all_deals = get_all_deals()
    budget_filtered = [
        deal
        for deal in all_deals
        if request.budget_min <= deal.price <= request.budget_max
    ]

    # Step 2: Mapping di keyword per categorie
    recipient_lower = request.recipient_description.lower()

    keyword_category_map: dict[str, dict[str, int]] = {
        # ===== GIOCHI E TOYS =====
        "dinosauri": {"toys": 10},
        "gioco": {"toys": 9},
        "giocattolo": {"toys": 10},
        "puzzle": {"toys": 9},
        "costruzioni": {"toys": 10},
        "robot": {"toys": 9, "electronics": 4},
        "giochi": {"toys": 10},
        "bambino": {"toys": 9, "fashion": 2},
        "bambini": {"toys": 9, "fashion": 2},
        "creativo": {"toys": 8},
        "educativo": {"toys": 8},
        "pattini": {"toys": 9},
        "disegno": {"toys": 8},
        "arte": {"toys": 7},
        "scienza": {"toys": 8},
        "laboratorio": {"toys": 9},

        # ===== TECH / GAMING / ELETTRONICA =====
        "tech": {"electronics": 10},
        "tecnologia": {"electronics": 10},
        "computer": {"electronics": 9},
        "gaming": {"electronics": 10},
        "gamer": {"electronics": 10},
        "cuffie": {"electronics": 10},
        "gadget": {"electronics": 10},
        "smartwatch": {"electronics": 9},
        "proiettore": {"electronics": 9},
        "speaker": {"electronics": 8},
        "tastiera": {"electronics": 9},
        "mouse": {"electronics": 8},
        "docking": {"electronics": 8},
        "sviluppatore": {"electronics": 9},
        "programmatore": {"electronics": 9},

        # ===== MODA / LIFESTYLE / SPORT =====
        "moda": {"fashion": 10},
        "abbigliamento": {"fashion": 10},
        "vestiti": {"fashion": 10},
        "abiti": {"fashion": 10},
        "outfit": {"fashion": 9},
        "look": {"fashion": 8},
        "stile": {"fashion": 8},
        "camicia": {"fashion": 9},
        "pantaloni": {"fashion": 9},
        "gonna": {"fashion": 9},
        "maglione": {"fashion": 9},
        "sneakers": {"fashion": 10},
        "scarpe": {"fashion": 10},
        "giacca": {"fashion": 10},
        "cappotto": {"fashion": 10},
        "accessori": {"fashion": 9},
        "borsa": {"fashion": 9},
        "cintura": {"fashion": 8},
        "zaino": {"fashion": 9},
        "beanie": {"fashion": 8},
        "sciarpa": {"fashion": 8},
        "sport": {"fashion": 9, "toys": 5},
        "corsa": {"fashion": 9},
        "runner": {"fashion": 9},

        # ===== BELLEZZA / SKINCARE / MAKEUP =====
        "bellezza": {"beauty": 10},
        "skincare": {"beauty": 10},
        "crema": {"beauty": 10},
        "creme": {"beauty": 10},
        "cosmetici": {"beauty": 10},
        "cosmetica": {"beauty": 10},
        "trucco": {"beauty": 10},
        "trucchi": {"beauty": 10},
        "makeup": {"beauty": 10},
        "rossetto": {"beauty": 9},
        "ombretto": {"beauty": 9},
        "mascara": {"beauty": 9},
        "siero": {"beauty": 9},
        "viso": {"beauty": 9},
        "pelle": {"beauty": 10},
        "corpo": {"beauty": 9},
        "profumo": {"beauty": 8},
        "donna": {"beauty": 8, "fashion": 5},
        "ragazza": {"beauty": 8, "fashion": 5},
        "benessere": {"beauty": 7},

        # ===== CASA / ARREDO =====
        "casa": {"home": 10},
        "arredo": {"home": 10},
        "salotto": {"home": 9},
        "soggiorno": {"home": 9},
        "cucina": {"home": 8},
        "bagno": {"home": 8},
        "camera": {"home": 8},
        "smart home": {"home": 10},
        "lampada": {"home": 8, "electronics": 3},
        "aspira": {"home": 10},
        "robot pulizia": {"home": 9},
        "termostato": {"home": 9},
        "diffusore": {"home": 8},
        "coperte": {"home": 8},
    }

        # Step 3: Calcola score per ogni prodotto
    scored_deals: list[tuple[Deal, int]] = []

    for deal in budget_filtered:
        score = 0

        # Controlla keyword mapping
        for keyword, category_scores in keyword_category_map.items():
            if keyword in recipient_lower:
                if deal.category.value in category_scores:
                    score += category_scores[deal.category.value]

        # Bonus per match diretti nel testo del prodotto
        deal_full_text = (deal.title + " " + deal.description).lower()
        recipient_words = set(recipient_lower.split())

        for word in recipient_words:
            if len(word) > 3 and word in deal_full_text:
                score += 3

        scored_deals.append((deal, score))

    # Step 4: tieni solo i prodotti con score > 0 (davvero rilevanti)
    filtered_scored_deals = [(deal, score) for deal, score in scored_deals if score > 0]

    # Se nessun prodotto è rilevante, restituisci lista vuota
    if not filtered_scored_deals:
        suggested: list[Deal] = []
    else:
        # Ordina per score decrescente
        filtered_scored_deals.sort(key=lambda x: x[1], reverse=True)
        # Estrai al massimo max_results prodotti
        suggested = [deal for deal, score in filtered_scored_deals[: request.max_results]]

    return AISuggestionResponse(
        recipient_description=request.recipient_description,
        suggested_deals=suggested,
        reasoning=(
            f"Suggerimenti personalizzati per '{request.recipient_description}' "
            f"con budget €{request.budget_min:.0f}-€{request.budget_max:.0f}. "
            "Mostrati solo prodotti considerati rilevanti."
        ),
    )


    # Step 4: Ordina per score decrescente
    scored_deals.sort(key=lambda x: x[1], reverse=True)

    # Step 5: Estrai top N risultati
    suggested = [deal for deal, score in scored_deals[: request.max_results]]

    return AISuggestionResponse(
        recipient_description=request.recipient_description,
        suggested_deals=suggested,
        reasoning=(
            f"Suggerimenti personalizzati per '{request.recipient_description}' "
            f"con budget €{request.budget_min:.0f}-€{request.budget_max:.0f}. Ordinati per rilevanza."
        ),
    )
