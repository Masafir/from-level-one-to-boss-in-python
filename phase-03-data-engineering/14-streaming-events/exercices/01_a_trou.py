"""
Module 14 — Exercice à trou #1
🎯 Thème : Le Concept du Stream Infini (Générateur Asynchrone)

En streaming, on ne lit pas un fichier entier fini. On écoute un topic qui recrache
une donnée à chaque événement. 

Complète les ___ pour créer ton premier générateur asynchrone ("Topic Kafka" du pauvre).
Exécute avec : python 01_a_trou.py
"""

import asyncio
import random
import time

# ============================================================
# 1. LE PRODUCTEUR ("Publisher" / "Topic")
# ============================================================

___ event_generator(): # Quel mot-clé pour définir une fonction asynchrone ?
    """Génère un flux infini d'événements de connexion de joueurs."""
    
    players = ["Alice", "Bob", "Charlie", "Diana"]
    actions = ["login", "login", "logout", "login"] # Biaisé vers login
    
    # Un stream c'est une boucle infinie !
    while ___: # Mettre à True pour infini
        event = {
            "player": random.choice(players),
            "action": random.choice(actions),
            "timestamp": time.time()
        }
        
        # En Python async, on "yield" la valeur au lieu de la return
        ___ event # Quel mot clé ?
        
        # On attend de l'I/O (Simulation de l'attente d'un nouvel event)
        await asyncio.___(0.3) # On attend 0.3s (Quelle fonction du module asyncio ?)

# ============================================================
# 2. LE CONSOMMATEUR ("Subscriber")
# ============================================================

async def process_stream():
    """Écoute le flux infini."""
    print("🎧 Démarrage de l'écoute du topic 'player_events'...")
    
    login_count = 0
    
    # Pour consommer un générateur ASYNCHRONE, on utilise "async for"
    ___ ___ event in event_generator(): # Quels mots clés ?
        
        if event["action"] == "login":
            print(f"🟢 {event['player']} s'est connecté.")
            login_count += 1
        else:
            print(f"🔴 {event['player']} s'est déconnecté.")
            
        # Pour les besoins de l'exercice, on va casser la boucle infinie après 5 logins
        if login_count >= 5:
            print("🛑 Fin du test : 5 logins détectés.")
            break 

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    # Point d'entrée de toute app Asyncio
    asyncio.___(process_stream()) # Quelle fonction pour lancer l'event loop ?
