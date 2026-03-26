"""
Module 18 — Exercice à trou #1
🎯 Thème : Le Logger d'Entreprise
On remplace tes mauvais `print()` par un vrai système de journalisation (logs).

Exécute avec : python 01_a_trou.py
"""

import ___ # 1. Import de la librairie standard (Pas besoin de pip install)

# ==========================================
# 2. CONFIGURATION GLOBALE
# ==========================================
# À appeler 1 seule fois, idéalement au tout début de ton `main.py`
logging.___( # Quelle fonction configure tout le bouzin (basic...) ?
    level=logging.___, # On veut voir les infos générales (pas tous les trucs de débogage cachés) (INFO)
    format="%(asctime)s [%(levelname)s] - %(message)s" 
)

# 3. CRÉATION DU LOGGER POUR CE FICHIER SPECIFIQUE
# Best practice : on utilise le nom du fichier actuel
logger = logging.___(__name__) # get logger


def faire_un_achat(joueur_id: int, montant: int):
    # Remplaçons: print("Achat en cours...")
    logger.___("Achat en cours...") # Quel niveau pour dire que tout va bien (info) ?
    
    if montant <= 0:
        # Remplaçons: print("ATTENTION: Montant nul ou négatif")
        logger.___("Montant anormal détecté.") # Quel niveau d'alerte intermédiaire (warning) ?
        
    try:
        # Simulation de la BDD
        1 / 0
    except Exception as e:
        # Au lieu du print, on log l'erreur AVEC LA STACK TRACE ENTIÈRE (exc_info=True)
        logger.___("Crash brutal pendant le paiement !", exc_info=___) # Quel niveau maximal (error), et quel booléen ?


if __name__ == "__main__":
    faire_un_achat(42, -500)
