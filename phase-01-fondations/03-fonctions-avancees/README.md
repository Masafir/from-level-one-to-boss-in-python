# Module 03 — Fonctions Avancées 🧙‍♂️

> **Objectif** : Maîtriser les fonctions Python au-delà du basique — closures, decorators, generators. Ce sont les outils qui séparent un dev Python junior d'un dev Python senior.

## 1. Fonctions : les bases (rappel rapide)

```python
# Définition classique
def attack(damage: int, multiplier: float = 1.0) -> float:
    """Calcule les dégâts d'une attaque."""
    return damage * multiplier

# Arguments nommés (keyword arguments)
# En JS tu passes un objet { damage: 10, multiplier: 2 }
# En Python tu nommes directement les arguments :
attack(damage=50, multiplier=1.5)
attack(50, multiplier=1.5)  # Positionnel puis nommé, OK
# attack(multiplier=1.5, 50)  ❌ Nommé puis positionnel, INTERDIT

# Valeurs par défaut (comme en JS)
def create_player(name: str, hp: int = 100, level: int = 1) -> dict:
    return {"name": name, "hp": hp, "level": level}

# ⚠️ PIÈGE CLASSIQUE : ne JAMAIS mettre un mutable comme valeur par défaut !
# ❌ MAUVAIS
def add_item_bad(item: str, inventory: list = []) -> list:
    inventory.append(item)  # La même liste est partagée entre tous les appels !
    return inventory

# ✅ BON
def add_item_good(item: str, inventory: list | None = None) -> list:
    if inventory is None:
        inventory = []
    inventory.append(item)
    return inventory
```

## 2. *args et **kwargs — Les rest/spread de Python

```python
# *args = collecte les arguments positionnels restants (comme ...args en JS)
def sum_scores(*scores: int) -> int:
    """Accepte un nombre variable d'arguments."""
    return sum(scores)

sum_scores(100, 200, 300)  # 600

# **kwargs = collecte les arguments nommés restants (comme les props en React !)
def create_character(name: str, **stats: int) -> dict:
    """Accepte des stats arbitraires."""
    return {"name": name, **stats}

create_character("Alice", hp=100, attack=50, defense=30)
# {"name": "Alice", "hp": 100, "attack": 50, "defense": 30}

# Combiner les deux
def game_action(action: str, *targets: str, **options: any) -> None:
    print(f"Action: {action}")
    print(f"Targets: {targets}")
    print(f"Options: {options}")

game_action("fireball", "goblin", "orc", damage=50, aoe=True)
# Action: fireball
# Targets: ('goblin', 'orc')
# Options: {'damage': 50, 'aoe': True}

# Spread/unpack dans les appels (comme ...array en JS)
stats = [10, 20, 30]
sum_scores(*stats)  # Équivalent à sum_scores(10, 20, 30)

config = {"hp": 100, "level": 5}
create_character("Bob", **config)  # Équivalent à create_character("Bob", hp=100, level=5)
```

## 3. Fonctions Lambda — Les arrow functions de Python

```python
# JS  : const double = (x) => x * 2
# Py  : 
double = lambda x: x * 2

# ⚠️ Les lambdas Python sont LIMITÉES à une seule expression
# Pas de bloc, pas de statements, pas de if/for complet
# Utilise-les principalement comme callbacks inline :

players = [{"name": "Alice", "score": 100}, {"name": "Bob", "score": 200}]

# Tri avec lambda (très courant)
sorted(players, key=lambda p: p["score"])

# Map avec lambda (mais préfère list comprehension)
list(map(lambda p: p["name"], players))
# Préfère : [p["name"] for p in players]
```

## 4. Closures — Les fonctions qui se souviennent

Une closure c'est une fonction qui "capture" des variables de son scope parent. Exactement comme en JavaScript !

```python
# Closure basique
def create_damage_calculator(base_damage: int):
    """Crée une fonction de calcul de dégâts avec un bonus fixe."""
    
    def calculate(multiplier: float) -> float:
        # base_damage est "capturé" depuis le scope parent
        return base_damage * multiplier
    
    return calculate

fire_damage = create_damage_calculator(50)
ice_damage = create_damage_calculator(30)

fire_damage(2.0)  # 100
ice_damage(1.5)   # 45

# Closure avec état (comme un useState React !)
def create_counter(initial: int = 0):
    count = initial
    
    def increment(amount: int = 1) -> int:
        nonlocal count  # ⚠️ Nécessaire pour modifier une variable du scope parent !
        count += amount
        return count
    
    def get() -> int:
        return count  # Lecture seule = pas besoin de nonlocal
    
    return increment, get

inc, get = create_counter(0)
inc()    # 1
inc(5)   # 6
get()    # 6
```

> 💡 **nonlocal** : En JS, tu peux modifier une variable du scope parent sans rien de spécial. En Python, tu dois déclarer `nonlocal` pour modifier (pas pour lire) une variable du scope englobant.

## 5. Decorators — Le superpower de Python 🌟

Un decorator est une fonction qui **enveloppe** une autre fonction pour ajouter un comportement. C'est comme un HOC (Higher-Order Component) en React, mais pour les fonctions !

### Decorator basique

```python
import time
from functools import wraps

def timer(func):
    """Mesure le temps d'exécution d'une fonction."""
    @wraps(func)  # Préserve le nom et la doc de la fonction originale
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️ {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def heavy_computation(n: int) -> int:
    """Calcule la somme des carrés."""
    return sum(i ** 2 for i in range(n))

# @timer c'est exactement pareil que :
# heavy_computation = timer(heavy_computation)

heavy_computation(1_000_000)
# ⏱️ heavy_computation took 0.1234s
```

### Decorator avec arguments

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator qui ré-essaie une fonction en cas d'échec."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"⚠️ Attempt {attempt} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_game_data(api_url: str) -> dict:
    """Simule un appel API qui peut échouer."""
    import random
    if random.random() < 0.5:
        raise ConnectionError("API timeout")
    return {"status": "ok"}
```

### Decorator de logging (très utile en prod)

```python
def log_calls(func):
    """Log chaque appel avec arguments et résultat."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"📞 {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  → {result!r}")
        return result
    return wrapper

@log_calls
def create_spell(name: str, damage: int, element: str = "neutral") -> dict:
    return {"name": name, "damage": damage, "element": element}

create_spell("Fireball", 50, element="fire")
# 📞 create_spell('Fireball', 50, element='fire')
#   → {'name': 'Fireball', 'damage': 50, 'element': 'fire'}
```

### Empiler les decorators

```python
@timer
@log_calls
def battle(player: str, enemy: str) -> str:
    # Simuler un combat
    return f"{player} defeats {enemy}!"

# Exécution : timer(log_calls(battle))
# L'ordre compte ! Le decorator le plus proche de la fonction est appliqué en premier
```

## 6. Generators — Les itérateurs paresseux 💤

Un generator produit des valeurs **une par une** (lazy evaluation). Au lieu de créer toute une liste en mémoire, il génère chaque valeur à la demande. C'est comme un iterateur infini.

```python
# Fonction normale : crée toute la liste en mémoire
def get_all_levels(max_level: int) -> list[int]:
    return [i for i in range(1, max_level + 1)]  # 1M éléments en mémoire !

# Generator : produit une valeur à la fois
def get_levels(max_level: int):
    """Génère les niveaux un par un."""
    level = 1
    while level <= max_level:
        yield level  # 'yield' au lieu de 'return' !
        level += 1

# Utilisation
for level in get_levels(5):
    print(f"Level {level}")
# Level 1, Level 2, ..., Level 5

# Generator infini (impossible avec une liste !)
def infinite_enemies():
    """Génère des ennemis à l'infini."""
    enemy_types = ["goblin", "orc", "troll", "dragon"]
    count = 0
    while True:
        yield f"{enemy_types[count % len(enemy_types)]}_{count}"
        count += 1

spawner = infinite_enemies()
next(spawner)  # "goblin_0"
next(spawner)  # "orc_1"
next(spawner)  # "troll_2"

# Generator expression (comme list comprehension mais lazy)
# List comprehension : [x**2 for x in range(1000000)]  ← 1M éléments en RAM
# Generator expression : (x**2 for x in range(1000000))  ← 0 élément en RAM !

total = sum(x**2 for x in range(1_000_000))  # Mémoire constante !
```

### Generators avancés : yield from

```python
def walk_dungeon():
    """Génère les salles d'un donjon."""
    yield from ["entrance", "corridor", "trap_room"]
    yield "boss_room"
    yield from ["treasure_room", "exit"]

list(walk_dungeon())
# ["entrance", "corridor", "trap_room", "boss_room", "treasure_room", "exit"]
```

### Quand utiliser un generator ?

| Situation | Utilise |
|-----------|---------|
| Petite collection, besoin d'accès par index | **list** |
| Grande collection, itération unique | **generator** |
| Pipeline de traitement de données | **generator** |
| Stream infini | **generator** |
| Besoin de `.append()`, `.sort()` etc. | **list** |

## 7. Fonctions utilitaires built-in avancées

```python
from itertools import chain, islice, groupby
from functools import reduce, partial

# --- itertools ---

# chain : concaténer des itérables
inventory = chain(["sword", "shield"], ["potion", "scroll"])
list(inventory)  # ["sword", "shield", "potion", "scroll"]

# islice : slicing pour les generators (et iterateurs)
first_5_enemies = list(islice(infinite_enemies(), 5))

# groupby : regrouper des éléments consécutifs identiques
# ⚠️ Les données DOIVENT être triées par la clé de groupement !
data = sorted(players, key=lambda p: p["class"])
for class_name, group in groupby(data, key=lambda p: p["class"]):
    print(f"{class_name}: {list(group)}")

# --- functools ---

# partial : pré-remplir des arguments (comme .bind() en JS)
def damage(base: int, multiplier: float, element: str) -> float:
    return base * multiplier

fire_damage = partial(damage, element="fire")
fire_damage(50, 1.5)  # damage(50, 1.5, element="fire")

# reduce : accumuler (comme .reduce() en JS)
from functools import reduce
total_hp = reduce(lambda acc, p: acc + p["hp"], players, 0)
# Mais en Python on préfère : sum(p["hp"] for p in players)
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **`*args, **kwargs`** | Comme `...args` et les props spread en JS/React |
| **Closures** | Fonctions qui capturent leur scope. `nonlocal` pour modifier |
| **Decorators** | HOC pour fonctions. `@wraps` toujours. Essentiels en prod. |
| **Generators** | `yield` au lieu de `return`. Lazy evaluation. Mémoire constante. |
| **`partial`** | Comme `.bind()` en JS |

---

➡️ **Maintenant, passe aux exercices dans `exercices/` !**
