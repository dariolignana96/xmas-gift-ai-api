
# 🎄 Xmas Gift AI Suggester

Progetto full‑stack personale: **API FastAPI + frontend HTML/CSS/JS vanilla** per generare suggerimenti regalo in base a descrizione del destinatario e budget.  

Tutto gira **in locale**, usa solo **mock data inventati** e una logica “AI” basata su keyword e punteggi, senza servizi esterni a pagamento.

---

## ✨ Caratteristiche principali

- **Backend FastAPI**
  - Endpoint REST (`/deals`, `/deals/category/{category}`, `/deals/search`, `/deals/ai-suggest`)
  - Modelli Pydantic per validazione input/output
  - Health check (`/health`) per verificare lo stato del backend

- **Frontend moderno**
  - Single page `frontend/index.html` con HTML + CSS glassmorphism + JavaScript vanilla
  - Form con descrizione destinatario, budget min/max e selettore “Max suggerimenti” con pulsanti `+ / −`
  - Badge di stato backend, spinner di caricamento, toast di errore, animazioni sulle card dei prodotti

- **Logica “AI” leggibile**
  - Mappa di keyword → categorie (beauty, toys, electronics, fashion, home)
  - Calcolo di uno **score** per ogni prodotto in base a:
    - parole chiave nella descrizione
    - parole presenti anche nel titolo/descrizione del prodotto
  - Vengono mostrati solo i prodotti con `score > 0`, ordinati per pertinenza

---

## 🛠 Stack Tecnologico

- **Linguaggio:** Python 3
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **Container:** Docker (Dockerfile per backend)
- **Orchestrazione locale:** Docker Compose
- **Orchestrazione cloud-ready:** Kubernetes (Deployment + Service)
- **Testing (future ready):** pytest, pytest‑asyncio, httpx
- **Extra librerie disponibili:** requests, beautifulsoup4, python‑dotenv, ollama (per eventuali evoluzioni)

---

## 📂 Struttura del progetto

```
xmas-gift-ai-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app, endpoint REST, logica di ranking
│   ├── models.py         # Modelli Pydantic (Deal, DealCategory, request/response)
│   └── mock_data.py      # Dataset mock con prodotti inventati e helper
├── frontend/
│   └── index.html        # Single page app con HTML/CSS/JS
├── k8s/
│   ├── deployment.yaml   # Deployment Kubernetes per il backend
│   └── service.yaml      # Service Kubernetes per esporre l'API nel cluster
├── tests/                # (opzionale) spazio per test pytest
├── Dockerfile            # Containerizzazione backend FastAPI
├── docker-compose.yml    # Orchestrazione locale (servizio API)
├── requirements.txt      # Dipendenze Python
├── .gitignore            # File da escludere da Git
└── README.md             # Questo file
```

---

## 🚀 Come eseguirlo in locale

### 1. Clona il repository

```
git clone https://github.com/dariolignana96/xmas-gift-ai-api.git
cd xmas-gift-ai-api
```

### 2. Crea e attiva un virtualenv (consigliato)

```
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Installa le dipendenze

```
pip install -r requirements.txt
```

### 4. Avvia il backend FastAPI

```
uvicorn app.main:app --reload
```

- API base: `http://127.0.0.1:8000`
- Docs Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

### 5. Avvia il frontend

**Opzione veloce:**  
Apri `frontend/index.html` con il browser (doppio click).

**Opzione con server statico:**

```
cd frontend
python -m http.server 5500
```

Poi apri `http://127.0.0.1:5500/index.html`.

---

### 🔹 Esecuzione con Docker (opzionale)

Se hai Docker installato, puoi avviare il backend containerizzato con:

```
docker compose up --build
```

L'API sarà raggiungibile su `http://localhost:8000` (documentazione automatica su `/docs`).

---

## 🧠 Dettagli sulla logica di ranking

- Filtra i prodotti per `budget_min <= prezzo <= budget_max`.
- Per ogni prodotto calcola uno **score**:
  - aggiunge punti se la descrizione contiene keyword mappate sulla categoria del prodotto  
    (es. “trucco, trucchi, skincare, cosmetici” → beauty; “gaming, tech, cuffie” → electronics; “vestiti, abiti, moda” → fashion, ecc.).
  - aggiunge punti extra se parole della descrizione (più di 3 lettere) compaiono anche nel titolo/descrizione del prodotto.
- Scarta i prodotti con `score == 0` (non rilevanti).
- Ordina quelli restanti per score decrescente e restituisce al massimo `max_results`.

Se nessun prodotto è rilevante, il backend restituisce una lista vuota e il frontend mostra un messaggio “Nessun prodotto rilevante trovato per questi criteri”.

---

## ☁️ Cloud / Kubernetes (ready)

Il progetto include manifest Kubernetes in `k8s/` per eseguire il backend in un cluster:

- `deployment.yaml` → definisce il Deployment `xmas-gift-api` (pod con il container backend).
- `service.yaml` → espone il Deployment tramite un Service interno su porta 8000.

Questi file sono pensati per mostrare familiarità con concetti base Kubernetes (Deployment, Service, label/selector) e possono essere adattati a qualsiasi cluster (minikube, kind, cloud).

---

## 🤝 Note per recruiter / reviewer

- Tutti i prodotti, testi marketing e URL nel dataset sono **inventati** e creati solo per scopi dimostrativi.
- Il progetto è pensato per mostrare:
  - design di API REST con FastAPI
  - integrazione frontend ↔ backend
  - gestione errori e UX (loading, toast, stato backend)
  - logica “AI” spiegabile e modificabile facilmente (keyword e score)
  - containerizzazione (Docker), orchestrazione locale (Docker Compose) e manifest Kubernetes di base
- Nessuno scraping reale o collegamento a servizi esterni viene eseguito di default: l’app funziona completamente in locale.

---

## 📜 Licenza e uso

Il codice del progetto è originale, pensato per essere utilizzato liberamente in contesti **open‑source** e didattici.  
Puoi clonarlo, modificarlo e adattarlo per i tuoi esperimenti o per mostrarlo in colloquio.
```