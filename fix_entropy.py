import json
import os
import sys

# Force l'encodage UTF-8 pour la sortie console sous Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE = "loom_consolidated_v102.json"

if not os.path.exists(FILE):
    print(f"ERROR : {FILE} introuvable dans le dossier actuel.")
else:
    with open(FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for event in data:
        # Correction Tchernobyl
        if event.get('label') == "Tchernobyl":
            event['value'] = 1000
            event['whoWhat'] = "URSS / Centrale Lenine"
        
        # Correction de l'Horloge 1991 (Détente) pour éviter le plongeon visuel
        # On lui donne 1150 (supérieur à 1000) pour que la courbe continue de monter
        if "17 min" in event.get('label', '') or (event.get('year') == 1991 and event.get('category') == "☢️ ENTROPIE"):
            event['value'] = 1150
            event['label'] = "Horloge: 17 min (Detente systemique)"
            event['whoWhat'] = "Bulletin of Atomic Scientists"
            event['description'] = "Fin de la Guerre Froide. Point de securite maximale. La complexite systemique continue de croitre malgré la détente politique."

    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("SUCCESS : Données enrichies et Entropie lissée pour v148.")
