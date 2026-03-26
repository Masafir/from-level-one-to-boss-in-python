"""
Module 10 — Exercice à trou #1
🎯 Thème : Bases de pytest — assertions, fixtures, parametrize

Complète les ___ pour que les tests passent.
Exécute avec : pytest 01_a_trou.py -v
"""

import pytest
from dataclasses import dataclass, field

# ============================================================
# Code à tester
# ============================================================

@dataclass
class Player:
    name: str
    hp: int = 100
    max_hp: int = 100
    level: int = 1
    xp: int = 0
    inventory: list[str] = field(default_factory=list)
    
    def take_damage(self, amount: int) -> int:
        actual = max(0, amount)
        self.hp = max(0, self.hp - actual)
        return actual
    
    def heal(self, amount: int) -> int:
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed
    
    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        threshold = self.level * 100
        if self.xp >= threshold:
            self.xp -= threshold
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            return True
        return False
    
    @property
    def is_alive(self) -> bool:
        return self.hp > 0


# ============================================================
# FIXTURES
# ============================================================

@pytest.___  # Quel decorator pour une fixture ?
def player():
    """Joueur de base pour les tests."""
    return Player(name="TestHero", hp=100, max_hp=100, level=1)


@pytest.fixture
def wounded_player():
    """Joueur blessé."""
    return Player(name="Wounded", hp=30, max_hp=100, level=5)


@pytest.fixture
def inventory_items():
    return ["sword", "shield", "potion", "potion", "key"]


# ============================================================
# TESTS BASIQUES
# ============================================================

def test_player_creation(___):  # Quel paramètre pour utiliser la fixture ?
    ___ player.name == "TestHero"  # Quel mot-clé d'assertion ?
    assert player.hp == 100
    assert player.level == 1


def test_player_take_damage(player):
    player.take_damage(25)
    assert player.hp == ___  # Combien de HP restants ?
    assert player.is_alive == True


def test_player_die(player):
    player.take_damage(150)
    assert player.hp == ___  # Clamp à quel minimum ?
    assert player.is_alive == ___  # Vivant ou mort ?


def test_player_heal(wounded_player):
    healed = wounded_player.heal(50)
    assert healed == ___  # Combien de HP récupérés ?
    assert wounded_player.hp == 80


def test_player_overheal(wounded_player):
    healed = wounded_player.heal(200)
    assert healed == ___  # Max heal = max_hp - current_hp
    assert wounded_player.hp == wounded_player.max_hp


# ============================================================
# TESTS D'EXCEPTIONS
# ============================================================

def test_negative_damage(player):
    """Les dégâts négatifs sont clampés à 0."""
    actual = player.take_damage(-10)
    assert actual == 0
    assert player.hp == 100


# ============================================================
# PARAMETRIZE
# ============================================================

@pytest.mark.___(  "damage,expected_hp", [  # Quel marker pour les cas multiples ?
    (0, 100),
    (10, 90),
    (50, 50),
    (100, 0),
    (200, 0),
])
def test_damage_values(player, damage, expected_hp):
    player.take_damage(damage)
    assert player.hp == expected_hp


@pytest.mark.parametrize("xp,should_level_up,expected_level", [
    (50, False, 1),
    (100, True, 2),    # Level 1 threshold = 100
    (99, False, 1),
])
def test_level_up(player, xp, should_level_up, expected_level):
    leveled = player.gain_xp(xp)
    assert leveled == should_level_up
    assert player.level == expected_level


# ============================================================
# TESTS AVANCÉS
# ============================================================

def test_level_up_heals(player):
    """Level up devrait full heal le joueur."""
    player.take_damage(50)
    assert player.hp == 50
    player.gain_xp(100)  # Level up !
    assert player.hp == player.max_hp  # Full heal


def test_inventory_fixture(inventory_items):
    assert ___( inventory_items) == 5  # Quelle built-in pour la taille ?
    assert inventory_items.count("potion") == 2


class TestPlayerCombat:
    """Grouper les tests liés dans une classe."""
    
    def test_combat_sequence(self):
        attacker = Player(name="Attacker")
        defender = Player(name="Defender")
        
        defender.take_damage(30)
        ___ defender.hp == 70  # Assertion
        
        defender.take_damage(30)
        assert defender.hp == 40
        
        defender.heal(20)
        assert defender.hp == 60
    
    def test_multiple_players_independent(self):
        p1 = Player(name="P1")
        p2 = Player(name="P2")
        
        p1.take_damage(50)
        assert p1.hp == 50
        assert p2.hp == ___  # P2 non affecté ?
