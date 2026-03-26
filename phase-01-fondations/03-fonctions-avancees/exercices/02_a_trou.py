"""
Module 03 — Exercice à trou #2
🎯 Thème : Decorators et Generators

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

import time
from functools import ___  # Quel import pour préserver le nom/doc de la fonction ?

# ============================================================
# PARTIE 1 : Créer des decorators
# ============================================================

def cooldown(seconds: float):
    """
    Decorator qui empêche d'appeler une fonction plus d'une fois
    par intervalle de 'seconds' secondes.
    Comme un debounce/throttle en JS !
    """
    def decorator(func):
        last_called = [0.0]  # On utilise une liste pour éviter nonlocal
        
        @___(func)  # Préserve le nom et la doc de func
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < seconds:
                remaining = seconds - elapsed
                print(f"  ⏳ Cooldown ! Attends encore {remaining:.1f}s")
                return ___  # Que retourner si en cooldown ?
            last_called[0] = time.___()  # Quelle fonction pour le timestamp actuel
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def count_calls(func):
    """
    Decorator qui compte le nombre d'appels à une fonction.
    Ajoute un attribut .call_count à la fonction.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"  📊 {func.___} appelée {wrapper.call_count} fois")
        return func(*args, **kwargs)
    
    wrapper.call_count = ___  # Valeur initiale du compteur ?
    return wrapper


def validate_types(**type_hints):
    """
    Decorator qui valide les types des arguments.
    Usage: @validate_types(name=str, damage=int)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Vérifier les kwargs
            for param_name, expected_type in type_hints.___():
                if param_name in kwargs:
                    value = kwargs[param_name]
                    if not isinstance(value, expected_type):
                        ___ TypeError(  # Quel mot-clé pour lever une exception ?
                            f"'{param_name}' doit être {expected_type.__name__}, "
                            f"pas {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Test des decorators
@cooldown(1.0)
@count_calls
def cast_spell(name: str, target: str) -> str:
    return f"✨ {name} lancé sur {target} !"

print("🪄 Test Cooldown + Count:")
print(cast_spell("Fireball", "Goblin"))
print(cast_spell("Ice Bolt", "Orc"))  # Cooldown !
time.sleep(1.1)
print(cast_spell("Thunder", "Dragon"))

@validate_types(name=str, damage=int)
def create_weapon(name: str, damage: int) -> dict:
    return {"name": name, "damage": damage}

print(f"\n⚔️ {create_weapon(name='Excalibur', damage=100)}")
try:
    create_weapon(name="Sword", damage="fifty")  # Erreur !
except TypeError as e:
    print(f"  ❌ {e}")


# ============================================================
# PARTIE 2 : Generators
# ============================================================

def dungeon_crawler(rooms: list[dict]):
    """
    Generator qui parcourt les salles d'un donjon une par une.
    Chaque salle a : name, enemies (int), treasure (bool)
    
    Yield chaque salle avec un message contextuel.
    """
    for i, room in ___(rooms, start=1):  # Quelle built-in pour index + valeur ?
        print(f"  🚪 Salle {i}/{len(rooms)} : {room['name']}")
        
        if room["enemies"] > 0:
            print(f"     ⚔️ {room['enemies']} ennemis !")
        
        if room["treasure"]:
            print(f"     💎 Trésor trouvé !")
        
        ___  room  # Quel mot-clé pour un generator ?


# Test dungeon crawler
dungeon = [
    {"name": "Entrance Hall", "enemies": 0, "treasure": False},
    {"name": "Dark Corridor", "enemies": 3, "treasure": False},
    {"name": "Treasury", "enemies": 1, "treasure": True},
    {"name": "Boss Room", "enemies": 1, "treasure": True},
]

print("\n🏰 Dungeon Crawl:")
for room in dungeon_crawler(dungeon):
    # On peut traiter chaque salle au fur et à mesure
    pass


def fibonacci_xp():
    """
    Generator infini qui produit des seuils d'XP
    basés sur la suite de Fibonacci : 1, 1, 2, 3, 5, 8, 13, 21...
    Multipliés par 100 : 100, 100, 200, 300, 500, 800, 1300...
    """
    a, b = 1, 1
    while ___:  # Comment rendre un generator infini ?
        ___ a * 100  # Produire la valeur
        a, b = b, a + b  # Prochains termes de Fibonacci


# Test fibonacci
print("\n📈 XP Thresholds (Fibonacci):")
xp_gen = fibonacci_xp()
for i in range(8):
    xp = ___(xp_gen)  # Quelle built-in pour obtenir la prochaine valeur ?
    print(f"  Level {i+2}: {xp} XP requis")


def loot_drop_generator(drop_table: dict[str, float]):
    """
    Generator qui simule des drops de loot.
    drop_table = {"sword": 0.3, "shield": 0.2, "potion": 0.4, "legendary": 0.1}
    Les probabilités doivent sommer à ~1.0
    """
    import random
    
    items = list(drop_table.___())  # Extraire les noms d'items
    weights = list(drop_table.___())  # Extraire les probabilités
    
    while True:
        # random.choices retourne une liste, on prend le premier
        drop = random.choices(items, weights=weights, k=1)[0]
        ___ drop


# Test loot drops
print("\n🎁 Loot Drops:")
loot = loot_drop_generator({
    "🗡️ sword": 0.3,
    "🛡️ shield": 0.2,
    "🧪 potion": 0.4,
    "👑 legendary": 0.1,
})

from collections import Counter
drops = [next(loot) for _ in range(50)]
distribution = Counter(drops)
for item, count in distribution.most_common():
    bar = "█" * count
    print(f"  {item:<20} {bar} ({count})")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
