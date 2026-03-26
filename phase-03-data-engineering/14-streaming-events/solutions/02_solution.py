"""Module 14 — Solution exercice à trou #2"""

import asyncio
import random

class MessageBroker:
    def __init__(self):
        self.subscribers: list[asyncio.Queue] = []
        
    def create_subscription(self):
        q = asyncio.Queue()
        self.subscribers.append(q)
        return q
        
    async def publish(self, message: dict):
        for q in self.subscribers:
            await q.put(message)

async def analytics_service(queue: asyncio.Queue):
    print("📈 Analytics Service Démarré.")
    total_kills = 0
    headshots = 0
    
    while True:
        event = await queue.get()
        
        if event is None:
            break
            
        if event.get("type") == "kill":
            total_kills += 1
            if event.get("headshot"):
                headshots += 1
                
        print(f"📈 Analytics | Headshot Rate : {(headshots/total_kills)*100:.1f}%")

async def trophy_service(queue: asyncio.Queue):
    print("🏆 Trophy Service Démarré.")
    
    while True:
        event = await queue.get()
        if event is None: break
            
        if event.get("type") == "kill" and event.get("headshot"):
            print(f"🏆 Trophy Unlock! 'BOOM HEADSHOT' for player!")

async def game_server(broker: MessageBroker):
    print("🎮 Game Server génère des Kills...")
    
    for _ in range(3):
        await asyncio.sleep(0.5)
        is_headshot = random.random() > 0.7 
        
        event = {"type": "kill", "headshot": is_headshot}
        print(f"🎮 SERVER -> Publish Kill (Headshot={is_headshot})")
        
        await broker.publish(event)
        
    await broker.publish(None)
    
async def main():
    broker = MessageBroker()
    
    queue_analytics = broker.create_subscription()
    queue_trophy = broker.create_subscription()
    
    await asyncio.gather(
        game_server(broker),
        analytics_service(queue_analytics),
        trophy_service(queue_trophy)
    )
    
    print("✅ Exercice 02 Terminé. L'Event Driven Architecture est fonctionnelle.")

if __name__ == "__main__":
    asyncio.run(main())
