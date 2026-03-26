"""
Module 14 — Exercice à trou #2
🎯 Thème : Fan-out Pattern (1 Publisher -> N Subscribers) avec asyncio.Queue

Le pattern Fan-Out est la base de Kafka. Un événement est généré, 
et PLUSIEURS micro-services le lisent (ex: Service Analytics, Service Trophées).

Complète les ___ pour créer cet Event Bus en mémoire.
Exécute avec : python 02_a_trou.py
"""

import asyncio
import random

# ============================================================
# LE BROKER (Mini "Kafka" en RAM)
# ============================================================

class MessageBroker:
    def __init__(self):
        # Liste de files d'attentes (queues). 1 queue par subscriber.
        self.subscribers: list[asyncio.Queue] = []
        
    def create_subscription(self):
        """Un nouveau service veut écouter ! On lui crée sa propre Queue."""
        q = asyncio.___() # Crée une Queue asyncio
        self.subscribers.append(q)
        return q
        
    async def publish(self, message: dict):
        """Envoie le message à TOUS les subscribers (Fan-out)."""
        for q in self.___: # Itère sur la liste des subscribers
            await q.___(message) # Quelle méthode de Queue pour "pousser" un item ?


# ============================================================
# SERVICES (Subscribers)
# ============================================================

async def analytics_service(queue: asyncio.Queue):
    """Calcule le % de headshots en temps réel."""
    print("📈 Analytics Service Démarré.")
    total_kills = 0
    headshots = 0
    
    while True:
        # On lit la queue bloquante (I/O). On attend le prochain msg.
        event = ___ queue.__() # await, et quelle method de Queue pour lire ?
        
        # Poison pill (Arrêt)
        if event is None:
            break
            
        if event.get("type") == "kill":
            total_kills += 1
            if event.get("headshot"):
                headshots += 1
                
        print(f"📈 Analytics | Headshot Rate : {(headshots/total_kills)*100:.1f}%")


async def trophy_service(queue: asyncio.Queue):
    """Débloque des trophées si besoin."""
    print("🏆 Trophy Service Démarré.")
    
    while True:
        event = await queue.get()
        if event is None: break
            
        if event.get("type") == "kill" and event.get("headshot"):
            print(f"🏆 Trophy Unlock! 'BOOM HEADSHOT' for player!")


# ============================================================
# SERVEUR DE JEU (Publisher)
# ============================================================

async def game_server(broker: MessageBroker):
    print("🎮 Game Server génère des Kills...")
    
    for _ in range(3): # 3 kills
        await asyncio.sleep(0.5)
        # 30% de chance que le kill soit un headshot
        is_headshot = random.random() > 0.7 
        
        event = {"type": "kill", "headshot": is_headshot}
        print(f"🎮 SERVER -> Publish Kill (Headshot={is_headshot})")
        
        # On publie sur le broker !
        await broker.___(event) # Quelle fonction de l'objet broker a été définie ?
        
    # Fin, on envoie le signal de Poison Pill à tous
    await broker.publish(None)
    

# ============================================================
# ORCHESTRATION
# ============================================================

async def main():
    broker = MessageBroker()
    
    # 1. On branche les subscribers (ils obtiennent leur propre Queue du broker)
    queue_analytics = broker.create_subscription()
    queue_trophy = broker.create_subscription()
    
    # 2. On lance TOUT EN MÊME TEMPS (Publisher + Les 2 Subscribers)
    await asyncio.gather(
        game_server(broker),
        analytics_service(queue_analytics),
        trophy_service(queue_trophy)
    )
    
    print("✅ Exercice 02 Terminé. L'Event Driven Architecture est fonctionnelle.")

if __name__ == "__main__":
    asyncio.run(main())
