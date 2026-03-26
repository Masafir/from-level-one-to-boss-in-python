"""
Module 03 — Exercice à trou #1
🎯 Thème : Closures et fonctions d'ordre supérieur

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

from functools import wraps

# ============================================================
# PARTIE 1 : *args et **kwargs
# ============================================================

def create_spell(name: str, ___damage: int, **___) -> dict:
    """
    Crée un sort avec un nom, des dégâts variables, et des propriétés bonus.
    *damage recevra les dégâts de chaque hit du sort.
    **props recevra les propriétés supplémentaires.
    """
    total_damage = ___(damage)  # Quelle fonction pour sommer ?
    return {
        "name": name,
        "total_damage": total_damage,
        "hits": ___(damage),  # Nombre de hits
        **props,              # Spread des props (comme React !)
    }

# Test
fireball = create_spell("Fireball", 30, 20, 15, element="fire", aoe=True)
print(f"🔥 {fireball}")
# {'name': 'Fireball', 'total_damage': 65, 'hits': 3, 'element': 'fire', 'aoe': True}

# Unpack une liste dans l'appel (comme spread en JS)
damages = [25, 30, 25, 20]
multi_hit = create_spell("Barrage", ___damages, element="physical")  # Comment unpack ?
print(f"⚔️ {multi_hit}")


# ============================================================
# PARTIE 2 : Closures
# ============================================================

def create_xp_tracker(level_thresholds: list[int]):
    """
    Closure qui track l'XP d'un joueur et gère le level up.
    
    level_thresholds = [100, 300, 600, 1000, 1500]
    signifie : level 2 à 100xp, level 3 à 300xp, etc.
    """
    current_xp = 0
    current_level = 1
    
    def gain_xp(amount: int) -> dict:
        ___  # Quel mot-clé pour modifier current_xp du scope parent ?
        ___  # Et pour current_level aussi ?
        
        current_xp += amount
        
        # Vérifier les level ups
        while (current_level - 1) < len(level_thresholds) and \
              current_xp >= level_thresholds[current_level - 1]:
            current_level += 1
            print(f"  🎉 LEVEL UP ! Niveau {current_level} !")
        
        return {"xp": current_xp, "level": current_level}
    
    def get_status() -> dict:
        # Calculer l'XP restant pour le prochain niveau
        if (current_level - 1) < len(level_thresholds):
            next_threshold = level_thresholds[current_level - 1]
            remaining = next_threshold - current_xp
        else:
            remaining = 0
        
        return {
            "level": current_level,
            "xp": current_xp,
            "xp_to_next": remaining,
        }
    
    return gain_xp, get_status

# Test
gain_xp, get_status = create_xp_tracker([100, 300, 600, 1000])

print("\n📊 XP Tracker:")
gain_xp(50)
print(f"  Status: {get_status()}")  # level 1, 50xp
gain_xp(60)  # Level up !
print(f"  Status: {get_status()}")  # level 2, 110xp
gain_xp(200)  # Level up !
print(f"  Status: {get_status()}")  # level 3, 310xp


# ============================================================
# PARTIE 3 : Fonctions d'ordre supérieur
# ============================================================

def apply_buffs(base_stats: dict[str, int], *buff_functions) -> dict[str, int]:
    """
    Applique une série de buffs (fonctions) aux stats de base.
    Chaque buff est une fonction qui prend un dict de stats et retourne un nouveau dict.
    """
    stats = base_stats.copy()
    
    for buff_fn in ___:  # Itérer sur les fonctions buff
        stats = ___(stats)  # Appeler chaque fonction buff
    
    return stats


# Créer des buffs sous forme de fonctions
def strength_buff(stats: dict[str, int]) -> dict[str, int]:
    result = stats.copy()
    result["attack"] = int(result["attack"] * 1.5)
    return result

def shield_buff(stats: dict[str, int]) -> dict[str, int]:
    result = stats.copy()
    result["defense"] = int(result["defense"] * 2.0)
    return result

# Closure pour créer des buffs paramétrables
def create_buff(stat: str, ___ : float):
    """Crée une fonction buff qui multiplie une stat par un multiplicateur."""
    def buff(stats: dict[str, int]) -> dict[str, int]:
        result = stats.copy()
        result[stat] = int(result[stat] * ___)  # Capture du scope parent
        return result
    return ___  # Retourner la fonction


# Test
base = {"attack": 50, "defense": 30, "speed": 40}

# Créer un buff de vitesse x3 avec la closure
speed_buff = create_buff("speed", ___)

# Appliquer les buffs
buffed = apply_buffs(base, strength_buff, shield_buff, speed_buff)
print(f"\n💪 Base: {base}")
print(f"💪 Buffed: {buffed}")
# attack: 75, defense: 60, speed: 120


# ============================================================
# PARTIE 4 : Composition de fonctions
# ============================================================

def compose(*functions):
    """
    Compose plusieurs fonctions : compose(f, g, h)(x) = f(g(h(x)))
    Comme pipe en RxJS mais inversé.
    """
    def composed(value):
        result = value
        # Appliquer les fonctions de droite à gauche
        for fn in ___(functions):  # Quelle fonction pour inverser ?
            result = fn(result)
        return result
    return composed


# Pipeline de transformation de données
def parse_score(raw: str) -> int:
    return int(raw.strip())

def apply_bonus(score: int) -> int:
    return int(score * 1.2)

def clamp_max(score: int) -> int:
    return ___(score, 99999)  # Quelle built-in pour limiter au maximum ?

# Composer les fonctions
process_score = compose(clamp_max, apply_bonus, parse_score)
print(f"\n🎯 Score: {process_score('  85000  ')}")  # 99999 (85000 * 1.2 = 102000, clamped)
print(f"🎯 Score: {process_score('  50000  ')}")  # 60000


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
