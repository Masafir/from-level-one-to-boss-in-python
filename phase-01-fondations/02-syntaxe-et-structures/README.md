# Module 02 — Syntaxe & Structures de Données 📦

> **Objectif** : Maîtriser les structures de données Python et la syntaxe idiomatique. C'est LE module qui te fera coder "pythoniquement" au lieu de coder du "JavaScript traduit en Python".

## 1. Les types de base

### Nombres

```python
# int — pas de limite de taille (contrairement à JS !)
big_number = 999_999_999_999  # Underscores pour la lisibilité
hex_val = 0xFF
bin_val = 0b1010

# float
pi = 3.14159
scientific = 1.5e10

# ⚠️ Pas de undefined ni de NaN en Python !
# None = le null de Python (comme null en JS, pas undefined)
value = None

# Vérifier None : utilise 'is', PAS '=='
if value is None:
    print("C'est None !")

# Division : attention aux différences !
print(10 / 3)    # 3.3333 (float division, comme JS)
print(10 // 3)   # 3 (integer division — N'EXISTE PAS en JS !)
print(10 % 3)    # 1 (modulo, pareil qu'en JS)
print(2 ** 10)   # 1024 (puissance — en JS c'est aussi ** )
```

### Strings

```python
# Single ou double quotes (pas de différence, comme en JS)
name = "Alice"
name = 'Alice'

# Multi-line strings (triple quotes)
story = """
Il était une fois
un développeur JavaScript
qui devint un Boss Python.
"""

# f-strings (le must — comme les template literals)
level = 42
msg = f"Niveau {level} atteint !"

# f-strings avancées
hp = 85
max_hp = 100
bar = f"HP: {hp}/{max_hp} ({hp/max_hp:.1%})"  # "HP: 85/100 (85.0%)"

# Alignement dans les f-strings
print(f"{'Nom':<15} {'Score':>10}")   # Aligné gauche / droite
print(f"{'Alice':<15} {15000:>10,}")  # "Alice           15,000"

# String methods utiles
text = "  Hello World  "
text.strip()          # Supprime les espaces → "Hello World"
text.lower()          # "  hello world  "
text.upper()          # "  HELLO WORLD  "
text.replace("World", "Python")
"hello world".split()           # ["hello", "world"]
", ".join(["a", "b", "c"])      # "a, b, c"
"hello".startswith("he")        # True
"python".endswith("on")         # True

# ⚠️ Les strings sont IMMUTABLES en Python (comme en JS)
# text[0] = "h"  → TypeError !
```

### Booléens et comparaisons

```python
# True / False (majuscule ! pas true/false comme en JS)
is_alive = True
is_dead = False

# Opérateurs logiques : and, or, not (pas &&, ||, !)
if is_alive and not is_dead:
    print("Le joueur est en vie")

# Valeurs "falsy" en Python (similaire à JS mais différent !)
# False, None, 0, 0.0, "", [], {}, set()
# ⚠️ En JS, [] et {} sont truthy. En Python, ils sont falsy !

empty_list = []
if not empty_list:  # True ! La liste vide est falsy
    print("Liste vide")

# Comparaisons chaînées (impossible en JS !)
x = 5
if 0 < x < 10:  # Équivalent : 0 < x and x < 10
    print("x est entre 0 et 10")

# is vs ==
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True (même valeur)
print(a is b)   # False (pas le même objet en mémoire)
# Utilise 'is' pour None : if x is None
```

## 2. Listes — Le Array de Python

```python
# Création
scores = [100, 250, 75, 300, 150]
mixed = [1, "hello", True, 3.14]  # Types mixtes (comme en JS)

# Accès (0-indexed, comme en JS)
first = scores[0]      # 100
last = scores[-1]       # 150 (index négatif = depuis la fin)
second_last = scores[-2] # 300

# Slicing (N'EXISTE PAS en JS — c'est un superpower Python !)
scores[1:3]     # [250, 75] — index 1 à 2 (3 exclu)
scores[:3]      # [100, 250, 75] — les 3 premiers
scores[2:]      # [75, 300, 150] — à partir de l'index 2
scores[::2]     # [100, 75, 150] — un sur deux (step=2)
scores[::-1]    # [150, 300, 75, 250, 100] — inversé !

# Modification
scores.append(500)        # Ajoute à la fin (.push() en JS)
scores.insert(0, 50)      # Insère au début (.unshift() en JS)
scores.extend([600, 700]) # Ajoute plusieurs (comme .concat() mais in-place)
scores.pop()              # Supprime et retourne le dernier
scores.pop(0)             # Supprime et retourne le premier (.shift() en JS)
scores.remove(75)         # Supprime la première occurrence par valeur

# Recherche
75 in scores              # True (comme .includes() en JS)
scores.index(250)         # Index de la valeur (comme .indexOf())
scores.count(100)         # Nombre d'occurrences

# Tri
scores.sort()             # Tri in-place (ascendant)
scores.sort(reverse=True) # Tri in-place (descendant)
sorted_scores = sorted(scores)  # Retourne une NOUVELLE liste triée

# Longueur
len(scores)  # Comme .length mais c'est une fonction, pas une propriété
```

## 3. List Comprehensions — Le superpower Python 💪

C'est LA feature qui va changer ta vie. Ça remplace `.map()`, `.filter()` et souvent les deux en une seule ligne.

```python
# JS : scores.map(s => s * 2)
# Python :
doubled = [s * 2 for s in scores]

# JS : scores.filter(s => s > 100)
# Python :
high_scores = [s for s in scores if s > 100]

# JS : scores.filter(s => s > 100).map(s => s * 2)
# Python : filtre ET transforme en une ligne !
boosted_high = [s * 2 for s in scores if s > 100]

# Avec des strings
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]
# ["ALICE", "BOB", "CHARLIE"]

# Avec condition ternaire (comme l'opérateur ternaire JS)
# JS  : scores.map(s => s > 100 ? "high" : "low")
# Py  :
labels = ["high" if s > 100 else "low" for s in scores]

# Nested comprehension (attention à la lisibilité !)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Dict comprehension
scores_dict = {f"player_{i}": s for i, s in enumerate(scores)}

# Set comprehension
unique_levels = {s // 100 for s in scores}  # Niveaux uniques
```

> 🧠 **Règle d'or** : Si ta list comprehension dépasse ~80 caractères ou est difficile à lire, utilise une boucle for classique. Le code lisible > le code compact.

## 4. Tuples — La liste immutable

```python
# Un tuple c'est comme une liste mais IMMUTABLE (on ne peut pas la modifier)
position = (10, 20)       # Coordonnées x, y
rgb = (255, 128, 0)       # Couleur

# Accès (comme une liste)
x = position[0]   # 10
y = position[1]   # 20

# Unpacking (destructuring en JS !)
# JS  : const [x, y] = position
# Py  :
x, y = position

# Multi-return (les fonctions Python peuvent retourner plusieurs valeurs !)
def get_player_stats():
    return "Alice", 100, 42  # Retourne un tuple implicitement

name, hp, level = get_player_stats()

# Swap sans variable temporaire (impossible en JS sans destructuring)
a, b = 1, 2
a, b = b, a  # a=2, b=1

# ⚠️ Tuple d'un seul élément : il faut une virgule !
single = (42,)    # Tuple
not_tuple = (42)  # Juste un int entre parenthèses !
```

## 5. Dictionnaires — Les objets Python

```python
# Création (comme les objets JS)
player = {
    "name": "Alice",
    "hp": 100,
    "level": 42,
    "inventory": ["sword", "shield"],
}

# Accès
player["name"]           # "Alice" (lève KeyError si absent !)
player.get("name")       # "Alice" (retourne None si absent)
player.get("mana", 0)    # 0 (valeur par défaut)

# Modification
player["hp"] = 95
player["mana"] = 50      # Ajoute une nouvelle clé

# Suppression
del player["mana"]
removed = player.pop("level")  # Supprime et retourne la valeur

# Vérifier si une clé existe
"name" in player         # True
"mana" in player         # False

# Itération
for key in player:                    # Itère sur les clés
    print(key)

for key, value in player.items():     # Clés et valeurs
    print(f"{key}: {value}")

for value in player.values():         # Valeurs seulement
    print(value)

# Merge (comme { ...obj1, ...obj2 } en JS)
defaults = {"hp": 100, "mana": 50, "level": 1}
custom = {"name": "Alice", "hp": 150}

# Python 3.9+ : l'opérateur |
merged = defaults | custom  # custom écrase defaults
# {"hp": 150, "mana": 50, "level": 1, "name": "Alice"}

# Ou avec ** (comme le spread mais pour les dicts)
merged = {**defaults, **custom}

# Dict comprehension
scores = {"Alice": 100, "Bob": 200, "Charlie": 150}
high_scorers = {name: score for name, score in scores.items() if score > 120}
# {"Bob": 200, "Charlie": 150}
```

## 6. Sets — L'ensemble unique

```python
# Un set = collection non ordonnée de valeurs UNIQUES
# Pas d'équivalent direct en JS (il y a Set mais on l'utilise peu)

unique_items = {"sword", "shield", "potion", "sword"}
# {"sword", "shield", "potion"} — le doublon est supprimé !

# Créer un set depuis une liste (dédoublonner)
items = ["sword", "shield", "sword", "potion", "shield"]
unique = set(items)  # {"sword", "shield", "potion"}

# Opérations ensemblistes (super puissant !)
team_a = {"Alice", "Bob", "Charlie"}
team_b = {"Bob", "Diana", "Eve"}

# Union (tous les joueurs)
all_players = team_a | team_b  # ou team_a.union(team_b)
# {"Alice", "Bob", "Charlie", "Diana", "Eve"}

# Intersection (joueurs dans les deux équipes)
common = team_a & team_b  # ou team_a.intersection(team_b)
# {"Bob"}

# Différence (joueurs dans A mais pas dans B)
only_a = team_a - team_b  # ou team_a.difference(team_b)
# {"Alice", "Charlie"}

# Test d'appartenance (ultra rapide, O(1) vs O(n) pour les listes !)
"Alice" in team_a  # True — utilise un set quand tu check souvent l'appartenance
```

## 7. Boucles et itération — La manière Pythonique

```python
# ❌ Manière "JavaScript traduite" (ne fais PAS ça en Python)
for i in range(len(scores)):
    print(scores[i])

# ✅ Manière Pythonique
for score in scores:
    print(score)

# ✅ Avec index ? Utilise enumerate (pas range(len()) !)
for i, score in enumerate(scores):
    print(f"#{i+1}: {score}")

# ✅ Deux listes en parallèle ? Utilise zip
names = ["Alice", "Bob", "Charlie"]
scores = [100, 200, 150]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# range() — comme un for(let i=0; i<n; i++)
for i in range(5):        # 0, 1, 2, 3, 4
    pass
for i in range(2, 8):     # 2, 3, 4, 5, 6, 7
    pass
for i in range(0, 10, 2): # 0, 2, 4, 6, 8 (step=2)
    pass

# while — pareil qu'en JS
hp = 100
while hp > 0:
    hp -= 10
    if hp == 50:
        continue  # Skip cette itération
    if hp == 20:
        break     # Sort de la boucle

# for...else (spécifique à Python — rare en pratique mais utile)
for item in inventory:
    if item == "key":
        print("Clé trouvée !")
        break
else:
    # S'exécute si la boucle n'a PAS été interrompue par break
    print("Pas de clé dans l'inventaire")
```

## 8. Fonctions de base essentielles

```python
# all() — tous les éléments sont truthy ?
all([True, True, True])   # True
all([True, False, True])  # False
all(score > 0 for score in scores)  # Tous positifs ?

# any() — au moins un élément truthy ?
any([False, False, True]) # True
any(score > 1000 for score in scores)  # Au moins un > 1000 ?

# map(), filter() — existent mais on préfère les list comprehensions
# map
list(map(str.upper, names))  # ["ALICE", "BOB"]
# Prefer: [name.upper() for name in names]

# filter
list(filter(lambda s: s > 100, scores))
# Prefer: [s for s in scores if s > 100]

# sorted() avec key
players = [
    {"name": "Alice", "score": 100},
    {"name": "Bob", "score": 300},
    {"name": "Charlie", "score": 200},
]
sorted(players, key=lambda p: p["score"], reverse=True)
# Trié par score décroissant

# enumerate() — index + valeur
for i, player in enumerate(players, start=1):
    print(f"#{i}: {player['name']}")

# zip() — combiner des itérables
dict(zip(["a", "b", "c"], [1, 2, 3]))
# {"a": 1, "b": 2, "c": 3}

# min(), max(), sum()
max(scores)                              # Plus grand
min(players, key=lambda p: p["score"])   # Player avec le plus petit score
sum(scores) / len(scores)               # Moyenne
```

---

## 🎯 Résumé

| Structure | Quand l'utiliser |
|-----------|-----------------|
| **list** `[]` | Collection ordonnée, modifiable |
| **tuple** `()` | Collection ordonnée, immutable (retours de fonctions, clés de dict) |
| **dict** `{}` | Associations clé-valeur (comme les objets JS) |
| **set** `{}` | Valeurs uniques, tests d'appartenance rapides |

| Pattern JS | Équivalent Python idomatique |
|------------|------------------------------|
| `.map(fn)` | `[fn(x) for x in list]` |
| `.filter(fn)` | `[x for x in list if fn(x)]` |
| `.forEach(fn)` | `for x in list:` |
| `.find(fn)` | `next((x for x in list if fn(x)), None)` |
| `.includes(v)` | `v in list` |
| `[...arr1, ...arr2]` | `[*arr1, *arr2]` |
| `{...obj1, ...obj2}` | `{**obj1, **obj2}` ou `obj1 \| obj2` |

---

➡️ **Maintenant, passe aux exercices dans `exercices/` !**
