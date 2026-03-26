"""
Module 14 — Exercice complet #3
🎯 Thème : Tumbling Window Aggregation (Fenêtres Temporelles)

Si le stream est infini, on ne peut pas faire un `.sum()` sur la BDD entière.
Il faut faire une somme "toutes les N secondes" (Tumbling Window).

Ton boss a besoin de connaitre le REVENU ($) GÉNÉRÉ TOUTES LES 2 SECONDES.
Le stream te donne 1 transaction par dixième de seconde (0.1s).

Exécute avec : python 03_exercice.py
"""

import asyncio
import random
import time

# ============================================================
# STREAM INFINI (Simulé)
# ============================================================
async def transaction_stream():
    """Génère 1 petite transaction aléatoire (de 1$ à 10$) toutes les 0.1s."""
    print("💸 Démarrage du stream des paiements...")
    for _ in range(80): # On s'arrête  au bout de ~8 secondes pour le test
        yield {"amount": random.randint(1, 10), "currency": "USD"}
        await asyncio.sleep(0.1)

# ============================================================
# TON EXERCICE : Tumbling Window Aggregator
# ============================================================

class TumblingWindowMetrics:
    def __init__(self, window_size_seconds: int):
        self.window_size = window_size_seconds
        
        # TODO : Initialiser ton état
        # 1. Tu as besoin d'une variable pour la somme des $ en cours
        # 2. Tu as besoin de sauvegarder le time.time() de départ de la fenêtre
        pass

    def add_event(self, event: dict):
        """
        Appelé à CHAQUE événement du stream.
        1. Vérifie si "maintenant" a dépassé la fenêtre (time.time() - start_time >= window)
        2. Si OUI : 
             Affiche dynamiquement le résultat avec un `print` clair !
             Remet la somme des $ à zéro.
             Réinitialise le start_time à "maintenant".
        3. Dans tous les cas, additionne le event["amount"] à la somme en cours.
        """
        # TODO : Ton code ici
        pass


# ============================================================
# CONSOMMATEUR
# ============================================================
async def process_financials():
    # Crée la mécanique de fenêtre pour 2 Secondes
    window = TumblingWindowMetrics(window_size_seconds=2)
    
    async for tx in transaction_stream():
        # A chaque Micro Transaction, on l'injecte dans la fenêtre
        window.add_event(tx)

if __name__ == "__main__":
    asyncio.run(process_financials())
    print("✅ Test de Windowing achevé.")
