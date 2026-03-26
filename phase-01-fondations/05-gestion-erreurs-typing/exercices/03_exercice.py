"""
Module 05 — Exercice complet #3
🎯 Thème : Système de sauvegarde de jeu robuste

Crée un système de save/load avec context managers, exceptions
custom et typing avancé.

Exécute avec : python 03_exercice.py
"""

from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar, Generic, Literal, Callable
from contextlib import contextmanager


# ============================================================
# PARTIE 1 : Exceptions custom pour le save system
# ============================================================

class SaveError(Exception):
    """
    TODO: Crée la hiérarchie d'exceptions :
    - SaveError (base)
    - CorruptedSaveError(SaveError) — fichier corrompu
    - SaveSlotFullError(SaveError) — plus de slots disponibles
    - SaveVersionError(SaveError) — version incompatible
    
    Chaque exception doit avoir des attributs utiles
    et un message descriptif.
    """
    pass


# ============================================================
# PARTIE 2 : Modèle de sauvegarde avec dataclasses
# ============================================================

@dataclass
class SaveMetadata:
    """
    TODO: Crée une dataclass pour les métadonnées de sauvegarde.
    
    Attributs :
    - slot_id: int
    - save_name: str
    - timestamp: float (time.time())
    - version: str (ex: "1.0.0")
    - playtime_seconds: float
    - checksum: str (pour détecter la corruption)
    """
    pass


@dataclass
class GameState:
    """
    TODO: Crée une dataclass pour l'état du jeu.
    
    Attributs :
    - player_name: str
    - level: int
    - hp: int
    - max_hp: int
    - inventory: list[str]
    - position: tuple[float, float]
    - quests_completed: list[str]
    - playtime: float
    
    Méthodes :
    - to_dict() -> dict : sérialiser en dict
    - from_dict(data: dict) -> GameState : désérialiser (@classmethod)
    - calculate_checksum() -> str : hash MD5 du contenu
    """
    pass


# ============================================================
# PARTIE 3 : Save Manager avec context managers
# ============================================================

class SaveManager:
    """
    TODO: Crée un gestionnaire de sauvegardes.
    
    Attributs :
    - save_dir: Path
    - max_slots: int (default 5)
    - current_version: str
    
    Méthodes :
    - save(slot_id, game_state, save_name) -> SaveMetadata
    - load(slot_id) -> GameState (avec validation)
    - delete(slot_id) -> None
    - list_saves() -> list[SaveMetadata]
    - get_save_path(slot_id) -> Path
    
    Context managers :
    - auto_save(game_state, interval) : sauvegarde automatique périodique
    - save_transaction(slot_id) : sauvegarde atomique avec rollback
    
    Le save doit :
    1. Vérifier que le slot est valide
    2. Créer un backup du slot existant
    3. Sauvegarder le nouveau state + metadata
    4. Calculer et stocker un checksum
    
    Le load doit :
    1. Vérifier que le fichier existe
    2. Vérifier le checksum (lever CorruptedSaveError si invalide)
    3. Vérifier la version (lever SaveVersionError si incompatible)
    4. Retourner le GameState
    """
    pass


# ============================================================
# PARTIE 4 : Event system typé
# ============================================================

# Types
EventType = Literal["save", "load", "delete", "error", "auto_save"]
EventCallback = Callable[[EventType, dict], None]

class SaveEventBus:
    """
    TODO: Crée un bus d'événements typé pour le save system.
    
    Méthodes :
    - on(event_type, callback) : enregistrer un listener
    - emit(event_type, data) : émettre un événement
    - off(event_type, callback) : retirer un listener
    """
    pass


# ============================================================
# MAIN — Tests
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("💾 SAVE SYSTEM — Tests")
    print("=" * 50)
    
    # Décommenter au fur et à mesure de l'implémentation
    
    # Test 1 : GameState
    # state = GameState(
    #     player_name="Alice", level=42, hp=95, max_hp=100,
    #     inventory=["sword", "shield", "potion"],
    #     position=(100.0, 250.0),
    #     quests_completed=["intro", "forest"],
    #     playtime=3600.0,
    # )
    # print(f"State: {state}")
    # print(f"Checksum: {state.calculate_checksum()}")

    # Test 2 : SaveManager
    # import tempfile
    # with tempfile.TemporaryDirectory() as tmp:
    #     manager = SaveManager(Path(tmp), max_slots=3)
    #
    #     # Save
    #     meta = manager.save(1, state, "My Save")
    #     print(f"\nSaved: {meta}")
    #
    #     # Load
    #     loaded = manager.load(1)
    #     print(f"Loaded: {loaded.player_name} Lv.{loaded.level}")
    #
    #     # List
    #     saves = manager.list_saves()
    #     print(f"Saves: {len(saves)}")
    #
    #     # Save transaction
    #     with manager.save_transaction(1) as path:
    #         print(f"Transaction on {path}")
    
    # Test 3 : Event bus
    # bus = SaveEventBus()
    # bus.on("save", lambda t, d: print(f"  🔔 {t}: {d}"))
    # bus.emit("save", {"slot": 1, "name": "My Save"})

    # Test 4 : Exceptions
    # try:
    #     manager.load(99)
    # except SaveError as e:
    #     print(f"❌ {e}")

    print("\n✅ Tests terminés !")
