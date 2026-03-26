# 🎮 Mini-Projet : Système de Buffs/Debuffs avec Decorators

## Objectif

Crée un framework de combat RPG complet où les **decorators** et **closures** sont au centre du système. Les sorts, buffs et debuffs sont tous des decorators qui modifient le comportement des abilités.

## Cahier des charges

### Architecture

```python
# Les abilités sont des fonctions décorées
@timed
@mana_cost(30)
@elemental("fire")
@buff_on_hit("attack", 1.2, duration=3)
@cooldown(seconds=2)
def fireball(caster: dict, target: dict) -> dict:
    """Lance une boule de feu."""
    return {"damage": caster["attack"] * 1.5, "type": "fire"}
```

### Decorators à implémenter

1. **@timed** — Log le temps d'exécution
2. **@mana_cost(amount)** — Vérifie et déduit le mana
3. **@cooldown(seconds)** — Empêche le spam de sort
4. **@elemental(element)** — Applique les bonus/malus élémentaires
5. **@buff_on_hit(stat, multiplier, duration)** — Applique un buff au caster quand le sort touche
6. **@debuff_on_hit(stat, multiplier, duration)** — Applique un debuff à la cible
7. **@combo_required(min_hits)** — Ne s'active que si le compteur de combo est suffisant
8. **@critical_chance(percent)** — Chance de coup critique (x2 damage)

### Closures à implémenter

1. **create_combat_logger()** — Log tous les événements de combat
2. **create_buff_manager()** — Gère la liste des buffs actifs (ajout, expiration, tick)
3. **create_mana_pool(max_mana, regen_rate)** — Pool de mana avec régénération

### Generators à implémenter

1. **turn_system(players)** — Alterne entre les joueurs (tour par tour)
2. **wave_spawner(config)** — Génère des vagues d'ennemis progressives
3. **buff_ticker(active_buffs)** — Tick les durées des buffs à chaque tour

### Système de combat

```python
# Simulation attendue
alice = {"name": "Alice", "hp": 100, "mana": 80, "attack": 30, "defense": 20}
goblin = {"name": "Goblin", "hp": 50, "mana": 0, "attack": 15, "defense": 10}

# Le combat utilise le turn system (generator)
for turn in turn_system([alice, goblin]):
    # Chaque tour, le joueur actif utilise une abilité
    result = fireball(turn["active"], turn["target"])
    print(f"Turn {turn['number']}: {result}")
```

## Critères de réussite ✅

- [ ] Au moins 5 decorators fonctionnels
- [ ] Decorators empilables (stackable)
- [ ] Système de mana avec closure
- [ ] Gestionnaire de buffs avec closure
- [ ] Turn system avec generator
- [ ] Simulation de combat fonctionnelle
- [ ] Code lisible et documenté
- [ ] Chaque decorator utilise `@wraps`

## Bonus 🌟

- Système de résistances élémentaires
- Decorator `@passive_ability` qui se déclenche automatiquement sous conditions
- Sauvegarde du combat log en JSON
- Statistiques de fin de combat (dégâts totaux, sorts lancés, etc.)
