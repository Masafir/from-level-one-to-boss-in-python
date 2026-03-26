# 🎮 Mini-Projet : Pokémon-like Data Analyzer

## Objectif

Crée un analyseur de données pour un jeu de type Pokémon ! Tu vas parser un fichier de données de créatures, les analyser et produire des rapports.

## Cahier des charges

### Les données

Tu vas travailler avec un "Pokédex" sous forme de liste de dictionnaires :

```python
creatures = [
    {"name": "Flamara", "type": "fire", "hp": 65, "attack": 130, "defense": 60, "speed": 65, "rarity": "rare"},
    {"name": "Aqualis", "type": "water", "hp": 130, "attack": 65, "defense": 60, "speed": 65, "rarity": "common"},
    {"name": "Voltix", "type": "electric", "hp": 65, "attack": 65, "defense": 60, "speed": 130, "rarity": "uncommon"},
    {"name": "Terrak", "type": "earth", "hp": 95, "attack": 110, "defense": 110, "speed": 45, "rarity": "rare"},
    # ... ajoute au moins 15 créatures
]
```

### Fonctionnalités à implémenter

1. **Stats par type** : moyenne de chaque stat par type d'élément
2. **Team builder** : trouver la meilleure équipe de 3 créatures (maximiser total stats)
3. **Matchup calculator** : simuler un combat basé sur les stats
4. **Rarity report** : distribution des raretés
5. **Power ranking** : classer toutes les créatures par "power score" (somme pondérée des stats)

### Formule de Power Score

```
power_score = (hp * 0.8) + (attack * 1.2) + (defense * 1.0) + (speed * 1.0)
```

### Format de sortie attendu

```
═══════════════════════════════════════
🔬 POKÉDEX ANALYZER — RAPPORT
═══════════════════════════════════════

📊 STATS PAR TYPE
─────────────────────────────────────
  🔥 fire    : HP:72  ATK:115  DEF:68  SPD:78
  💧 water   : HP:110 ATK:75   DEF:72  SPD:70
  ⚡ electric: HP:60  ATK:70   DEF:55  SPD:120

🏆 POWER RANKING (Top 5)
─────────────────────────────────────
  #1  Terrak     — 360.0 pts (earth)
  #2  Flamara    — 329.0 pts (fire)
  ...

👥 MEILLEURE ÉQUIPE
─────────────────────────────────────
  Terrak (earth) + Flamara (fire) + Voltix (electric)
  Total power: 958.0

⚔️ COMBAT : Flamara vs Aqualis
─────────────────────────────────────
  Flamara : ATK 130 vs DEF 60 → 70 dmg
  Aqualis : ATK 65 vs DEF 60 → 5 dmg
  Winner : Flamara ! 🏆
```

## Contraintes

- Utilise **uniquement** les structures vues dans le cours (list, dict, set, tuple)
- Utilise les **list/dict comprehensions** au maximum
- Utilise `sorted()`, `min()`, `max()`, `sum()`, `enumerate()`, `zip()`
- Pas de classes (on verra ça au Module 04)

## Bonus 🌟

- Ajoute un système de types avec avantages/désavantages (fire > earth > electric > water > fire)
- Implémente un mini-tournoi entre toutes les créatures
- Exporte les résultats en JSON

## Critères de réussite ✅

- [ ] Au moins 15 créatures dans le Pokédex
- [ ] Stats par type correctement calculées
- [ ] Power ranking correct
- [ ] Team builder fonctionne
- [ ] Simulation de combat basique
- [ ] Code propre avec des list comprehensions
- [ ] Affichage formaté
