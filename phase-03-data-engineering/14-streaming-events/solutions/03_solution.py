"""Module 14 — Solution exercice 3"""

import asyncio
import random
import time

async def transaction_stream():
    """Génère 1 petite transaction aléatoire (de 1$ à 10$) toutes les 0.1s."""
    print("💸 Démarrage du stream des paiements...")
    for _ in range(80): # On s'arrête au bout de ~8 secondes pour le test
        yield {"amount": random.randint(1, 10), "currency": "USD"}
        await asyncio.sleep(0.1)

class TumblingWindowMetrics:
    def __init__(self, window_size_seconds: int):
        self.window_size = window_size_seconds
        self.current_sum = 0
        self.start_time = time.time()

    def add_event(self, event: dict):
        now = time.time()
        
        if now - self.start_time >= self.window_size:
            print(f"📊 [WINDOW] Revenu total sur les {self.window_size} dernières secondes : {self.current_sum}$")
            self.current_sum = 0
            self.start_time = now
            
        self.current_sum += event.get("amount", 0)

async def process_financials():
    window = TumblingWindowMetrics(window_size_seconds=2)
    
    async for tx in transaction_stream():
        window.add_event(tx)

if __name__ == "__main__":
    asyncio.run(process_financials())
    print("✅ Test de Windowing achevé.")
