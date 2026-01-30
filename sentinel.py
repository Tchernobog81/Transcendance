import os
import json
import requests
import feedparser
import random
import zlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration
CLOUD_URL = os.getenv("CLOUD_URL")
# Si tu as une clé Gemini, elle sera utilisée ici
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") 

FEEDS = [
    "https://news.google.com/rss/search?q=singularité+technologique+IA+biotech&hl=fr&gl=FR&ceid=FR:fr",
    "https://www.technologyreview.com/feed/",
    "https://wired.com/feed/rss"
]

def analyze_event(title, summary, link):
    """
    Analyse l'événement. v148 : Déterminisme et pas de N/A.
    """
    seed_val = zlib.crc32(title.encode('utf-8'))
    random.seed(seed_val)
    
    # Heuristique de catégorie simplifiée
    category = "?? COGNITION"
    if any(word in title.lower() for word in ["spacex", "mars", "orbite"]): category = "?? ESPACE"
    elif any(word in title.lower() for word in ["crispr", "adn", "bio"]): category = "?? BIOTECH"
    elif any(word in title.lower() for word in ["menace", "risque", "climat", "guerre"]): category = "?? ENTROPIE"
    
    # Pharmakon Analysis (v148)
    remedy = random.randint(30, 70)
    if category == "?? ENTROPIE": remedy = random.randint(5, 20)
    
    event = {
        "year": datetime.now().year + (datetime.now().month / 12),
        "value": 15000 + random.randint(0, 5000), # Positionnement sur l'axe Y (Haut de courbe)
        "label": title[:50] + "...",
        "category": category,
        "whoWhat": "Sentinel Monitoring",
        "description": summary[:200] + "...",
        "url": link,
        "timestamp": datetime.now().isoformat(),
        "s_curve_phase": 4,
        "pharmakon_remedy_percent": remedy,
        "pharmakon_poison_percent": 100 - remedy,
        "convergences": f"Signal détecté en {category}. Convergence systémique automatique.",
        "grand_filter_analysis": "Analyse en attente de traitement profond par l'Exocortex."
    }
    return event

def run_veille():
    print("--- TRANSCENDANCE SENTINEL Beta 1.2.5 : START VEILLE ---")
    if not CLOUD_URL:
        print("Erreur : CLOUD_URL manquante.")
        return

    new_events = []
    for url in FEEDS:
        print(f"Scanning feed: {url[:50]}...")
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # On prend les 3 plus récents par flux
            event = analyze_event(entry.title, entry.get('summary', ''), entry.link)
            new_events.append(event)

    if new_events:
        print(f"Injection de {len(new_events)} signaux vers le Cloud...")
        res = requests.post(CLOUD_URL, json=new_events, timeout=60)
        print(f"Status: {res.status_code}, Response: {res.text}")

if __name__ == "__main__":
    run_veille()
