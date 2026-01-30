import requests
import json
import os
import random
import zlib
import sys

# Gestion de l'encodage pour la console Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERREUR CRITIQUE : Module 'python-dotenv' manquant.")
    print("--> Veuillez exécuter : pip install requests python-dotenv")
    sys.exit(1)

# Charge la configuration depuis le fichier .env
load_dotenv()
CLOUD_URL = os.environ.get("CLOUD_URL")
DATA_FILE = "loom_consolidated_v102.json"

def enrich_event_if_needed(event):
    """
    Enrichit un événement avec des données analytiques (Pharmakon, S-Curve)
    si elles sont manquantes. Déterministe via le label.
    """
    # Si l'analyse existe déjà, on ne touche à rien
    if "s_curve_phase" in event and event.get("s_curve_phase") is not None:
        return event

    label = event.get('label', '')
    year = event.get("year", 1900)
    category = event.get("category", "DEFAUT")

    # 0. Déterminisme : Le hash du label sert de graine aléatoire
    seed_val = zlib.crc32(label.encode('utf-8'))
    random.seed(seed_val)

    # 1. Phase de la courbe en S selon l'année
    if year < 1940: s_curve_phase = 1
    elif year < 1990: s_curve_phase = 2
    elif year < 2015: s_curve_phase = 3
    elif year < 2030: s_curve_phase = 4
    else: s_curve_phase = 5

    # 2. Analyse Pharmakon par catégorie
    remedy = 50
    if "ENTROPIE" in category: remedy = 10
    elif "BIOTECH" in category or "NOOSPHÈRE" in category: remedy = 75
    elif "HARDWARE" in category or "COGNITION" in category: remedy = 65
    elif "POLITIQUE" in category: remedy = 35
    elif "IMAGINAIRE" in category: remedy = 50

    # Variation aléatoire stable
    remedy += random.randint(-10, 10)
    remedy = max(5, min(95, remedy))
    poison = 100 - remedy

    # 3. Ajout des champs
    event["s_curve_phase"] = s_curve_phase
    event["pharmakon_remedy_percent"] = remedy
    event["pharmakon_poison_percent"] = poison
    
    random.seed() # Reset
    return event

def inject_massive_data():
    print(f"--- TRANSCENDANCE : INJECTION v148 ---")
    
    if not CLOUD_URL:
        print("ERROR: CLOUD_URL manquante dans le fichier .env")
        return

    if not os.path.exists(DATA_FILE):
        print(f"ERROR: Fichier '{DATA_FILE}' introuvable.")
        return

    print(f"Reading {DATA_FILE}...")
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Enrichissement des données (Pharmakon/S-Curve)...")
        for event in data:
            enrich_event_if_needed(event)
            
        # Sauvegarde locale pour garder la trace
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Sending {len(data)} events to Transcendance Cloud...")
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(CLOUD_URL, data=json.dumps(data), headers=headers, timeout=60)
        
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('status') == 'ok' or res_json.get('result') == 'success':
                print(f"SUCCESS : Base de données synchronisée.")
                print(f"Items: {res_json.get('items') or res_json.get('count')}")
            else:
                print(f"Server Logic Error: {res_json}")
        else:
            print(f"HTTP Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Crash: {e}")

if __name__ == "__main__":
    inject_massive_data()