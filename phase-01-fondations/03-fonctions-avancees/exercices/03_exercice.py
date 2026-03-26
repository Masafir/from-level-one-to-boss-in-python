"""
Module 03 — Exercice complet #3
🎯 Thème : Système de buffs/debuffs avec decorators et closures

Objectif : Créer un système de buffs/debuffs pour un jeu RPG
utilisant des decorators, closures et generators.

Exécute avec : python 03_exercice.py
"""

import time
from functools import wraps


# ============================================================
# PARTIE 1 : Decorator @timed_ability
# ============================================================

def timed_ability(func):
    """
    TODO: Crée un decorator qui :
    1. Affiche le nom de l'abilité utilisée
    2. Mesure le temps d'exécution
    3. Affiche le résultat

    Exemple de sortie :
      ⚡ Using: Fireball
      → Result: 75 damage dealt
      ⏱️ 0.001s

    Hints:
    - Utilise time.perf_counter() pour mesurer
    - func.__name__ pour le nom
    - @wraps(func) pour préserver les métadonnées
    """
    pass  # Remplace par ton implémentation


# ============================================================
# PARTIE 2 : Decorator factory @buff
# ============================================================

def buff(stat: str, multiplier: float, duration: int = 3):
    """
    TODO: Crée un decorator factory qui applique un buff à une abilité.

    Le decorator doit :
    1. Modifier le résultat de la fonction en multipliant la stat donnée
    2. Tracker le nombre d'utilisations restantes (duration)
    3. Quand le buff expire (uses restants = 0), appliquer la fonction normalement
    4. Afficher un message quand le buff est actif/expiré

    Exemple :
      @buff("damage", 2.0, duration=3)
      def slash(target):
          return {"damage": 25, "target": target}

      slash("goblin")  # → {"damage": 50, "target": "goblin"} (buffé x2)
      slash("goblin")  # → {"damage": 50, "target": "goblin"} (buffé x2)
      slash("goblin")  # → {"damage": 50, "target": "goblin"} (buffé x2)
      slash("goblin")  # → {"damage": 25, "target": "goblin"} (buff expiré)

    Hints:
    - Utilise une liste [duration] pour le compteur mutable dans la closure
    - Le résultat de func() est un dict, modifie la clé 'stat'
    """
    pass  # Remplace par ton implémentation


# ============================================================
# PARTIE 3 : Closure — Combo Counter
# ============================================================

def create_combo_system(combo_multipliers: dict[int, float]):
    """
    TODO: Crée un système de combo avec closure.

    combo_multipliers définit le multiplicateur par nombre de hits :
    {1: 1.0, 2: 1.2, 3: 1.5, 5: 2.0, 10: 3.0}

    Le système doit :
    1. Tracker le combo count actuel
    2. Retourner une fonction 'hit' qui :
       - Incrémente le combo
       - Applique le multiplicateur le plus élevé applicable
       - Retourne le damage modifié et le combo actuel
    3. Retourner une fonction 'reset' qui remet le combo à 0
    4. Retourner une fonction 'get_combo' qui retourne le combo actuel

    Exemple :
      hit, reset, get_combo = create_combo_system({1: 1.0, 3: 1.5, 5: 2.0})
      hit(10)  # {"damage": 10, "combo": 1, "multiplier": 1.0}
      hit(10)  # {"damage": 10, "combo": 2, "multiplier": 1.0}
      hit(10)  # {"damage": 15, "combo": 3, "multiplier": 1.5}

    Hints:
    - Utilise nonlocal pour modifier le compteur
    - max(k for k in multipliers if k <= combo) pour trouver le bon multiplicateur
    """
    pass  # Remplace par ton implémentation


# ============================================================
# PARTIE 4 : Generator — Buff Timeline
# ============================================================

def buff_timeline(*buffs: dict):
    """
    TODO: Generator qui simule une timeline de buffs.

    Chaque buff est un dict : {"name": str, "stat": str, "value": float, "duration": int}

    Le generator doit :
    1. À chaque tour (yield), retourner les buffs actifs et leur effet total
    2. Décrémenter la durée de chaque buff
    3. Retirer les buffs expirés
    4. S'arrêter quand tous les buffs ont expiré

    Yield un dict à chaque tour :
    {
        "turn": 1,
        "active_buffs": ["Power Up", "Shield"],
        "effects": {"attack": 1.5, "defense": 2.0},
        "expired": []
    }

    Hints:
    - Copie les buffs dans une liste mutable au début
    - Utilise une boucle while len(active_buffs) > 0
    - À chaque itération : yield → décrémenter → retirer expirés
    """
    pass  # Remplace par ton implémentation


# ============================================================
# PARTIE 5 : Tout assembler
# ============================================================

def create_ability(name: str, base_damage: int, element: str = "neutral"):
    """
    TODO: Crée une abilité de combat qui utilise tes systèmes ci-dessus.

    Retourne une fonction qui, quand appelée avec une cible :
    1. Calcule les dégâts de base
    2. Retourne un dict avec name, damage, element, target

    C'est une simple closure, pas besoin de decorator ici.
    """
    pass  # Remplace par ton implémentation


# ============================================================
# MAIN — Tests
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("⚔️ RPG BUFF/DEBUFF SYSTEM — Tests")
    print("=" * 50)

    # Test 1 : Timed ability
    print("\n--- Test 1 : @timed_ability ---")
    if timed_ability.__class__.__name__ != "NoneType":
        @timed_ability
        def fireball(target: str) -> dict:
            return {"damage": 75, "element": "fire", "target": target}

        result = fireball("Dragon")
        if result:
            print(f"  Result: {result}")

    # Test 2 : Buff decorator
    print("\n--- Test 2 : @buff ---")
    if buff.__class__.__name__ != "NoneType":
        @buff("damage", 2.0, duration=2)
        def slash(target: str) -> dict:
            return {"damage": 25, "target": target}

        for i in range(4):
            result = slash(f"enemy_{i}")
            if result:
                print(f"  Hit {i+1}: {result}")

    # Test 3 : Combo system
    print("\n--- Test 3 : Combo System ---")
    combo_result = create_combo_system({1: 1.0, 3: 1.5, 5: 2.0, 10: 3.0})
    if combo_result:
        hit, reset, get_combo = combo_result
        for i in range(7):
            result = hit(10)
            print(f"  Hit {i+1}: {result}")
        print(f"  Reset!")
        reset()
        print(f"  Combo after reset: {get_combo()}")

    # Test 4 : Buff timeline
    print("\n--- Test 4 : Buff Timeline ---")
    timeline = buff_timeline(
        {"name": "Power Up", "stat": "attack", "value": 1.5, "duration": 3},
        {"name": "Shield", "stat": "defense", "value": 2.0, "duration": 2},
        {"name": "Haste", "stat": "speed", "value": 1.8, "duration": 4},
    )
    if timeline:
        for turn_info in timeline:
            if turn_info:
                active = ", ".join(turn_info.get("active_buffs", []))
                expired = ", ".join(turn_info.get("expired", []))
                print(f"  Turn {turn_info['turn']}: [{active}]" +
                      (f" | Expired: {expired}" if expired else ""))

    print("\n✅ Tests terminés !")
