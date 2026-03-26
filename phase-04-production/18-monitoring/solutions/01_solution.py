"""Module 18 — Solution exercice à trou #1"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s" 
)

logger = logging.getLogger(__name__)

def faire_un_achat(joueur_id: int, montant: int):
    logger.info("Achat en cours...")
    
    if montant <= 0:
        logger.warning("Montant anormal détecté.")
        
    try:
        1 / 0
    except Exception as e:
        logger.error("Crash brutal pendant le paiement !", exc_info=True)


if __name__ == "__main__":
    faire_un_achat(42, -500)
