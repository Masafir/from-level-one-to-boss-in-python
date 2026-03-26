"""
Module 18 — Exercice à trou #2
🎯 Thème : Sentry Integration dans FastAPI
On configure Sentry pour attraper toutes les erreurs 500 automatically.
"""

from fastapi import FastAPI
import ___ # 1. Import du SDK sentry (sentry_sdk) 

# ==========================================
# 2. CONFIGURATION DE SENTRY
# ==========================================
sentry_sdk.___( # Quelle fonction d'initialisation appelle-t-on (init) ?
    dsn="https://fake_key@o22222.ingest.sentry.io/44444",
    # On veut analyser la vitesse de 10% de nos requêtes (Performance Monitoring)
    traces_sample_rate=___, # 10% (0.1)
    
    # On précise bien l'environnement 
    environment="___" # Ex: production
)

# Une fois Sentry instancié, TOUT crash dans l'application FastAPI partira
# sur leur plateforme cloud !
app = ___()

@app.get("/acheter-epee")
def fake_crash():
    # Sentry verra exactement sur quelle ligne cette erreur s'est produite,
    # ET verra toutes les variables du scope dans l'UI (comme "item"). Magique.
    item = "Epée de feu"
    is_admin = False
    
    # BOUM
    raise ValueError("Le solde du joueur est insuffisant !")
    
    return {"msg": "Acheté"}
