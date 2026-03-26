"""Module 14 — Solution exercice à trou #1"""

import asyncio
import random
import time

async def event_generator():
    players = ["Alice", "Bob", "Charlie", "Diana"]
    actions = ["login", "login", "logout", "login"]
    
    while True:
        event = {
            "player": random.choice(players),
            "action": random.choice(actions),
            "timestamp": time.time()
        }
        
        yield event
        
        await asyncio.sleep(0.3)

async def process_stream():
    print("🎧 Démarrage de l'écoute du topic 'player_events'...")
    
    login_count = 0
    
    async for event in event_generator():
        if event["action"] == "login":
            print(f"🟢 {event['player']} s'est connecté.")
            login_count += 1
        else:
            print(f"🔴 {event['player']} s'est déconnecté.")
            
        if login_count >= 5:
            print("🛑 Fin du test : 5 logins détectés.")
            break 

if __name__ == "__main__":
    asyncio.run(process_stream())
