"""
Module 09 — Exercice à trou #1
🎯 Thème : JWT, hashing et authentification

Complète les ___ pour que le code fonctionne.
Exécute avec : pip install passlib[bcrypt] python-jose[cryptography]
              python 01_a_trou.py
"""

from datetime import datetime, timedelta
from passlib.context import CryptContext

# ============================================================
# PARTIE 1 : Hashing de mots de passe
# ============================================================

# Créer le context bcrypt
pwd_context = ___(schemes=["bcrypt"], deprecated="auto")  # Quel objet passlib ?

def hash_password(password: str) -> str:
    return pwd_context.___(password)  # Quelle méthode pour hasher ?

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.___(plain, hashed)  # Quelle méthode pour vérifier ?


# Test
password = "super_secret_123"
hashed = hash_password(password)
print(f"🔒 Hash: {hashed[:30]}...")
print(f"✅ Verify correct: {verify_password(password, hashed)}")
print(f"❌ Verify wrong: {verify_password('wrong', hashed)}")


# ============================================================
# PARTIE 2 : JWT
# ============================================================

# Pas de python-jose dans cet exercice, on simule avec un dict encodé
# pour que l'exercice fonctionne sans dépendances lourdes

import json
import base64
import hashlib

SECRET_KEY = "my-super-secret-key"

def create_token(data: dict, expires_minutes: int = 30) -> str:
    """Crée un token simlifié (en vrai, utilise python-jose)."""
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload["exp"] = expire.___()  # Quelle méthode pour convertir datetime en string ISO ?
    
    # Encoder en base64 (simplifié)
    payload_json = json.dumps(payload)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode()
    
    # Signer avec HMAC
    signature = hashlib.sha256(
        f"{payload_b64}.{SECRET_KEY}".encode()
    ).hexdigest()[:32]
    
    return f"{payload_b64}.{signature}"


def decode_token(token: str) -> dict:
    """Décode et vérifie un token."""
    parts = token.split(".")
    if ___(parts) != 2:  # Combien de parties attendues ?
        raise ValueError("Token malformé")
    
    payload_b64, signature = parts
    
    # Vérifier la signature
    expected_sig = hashlib.sha256(
        f"{payload_b64}.{SECRET_KEY}".encode()
    ).hexdigest()[:32]
    
    if signature ___ expected_sig:  # Quel opérateur pour "différent de" ?
        raise ValueError("Signature invalide")
    
    # Décoder
    payload_json = base64.urlsafe_b64decode(payload_b64).decode()
    payload = json.loads(payload_json)
    
    # Vérifier l'expiration
    exp = datetime.fromisoformat(payload["exp"])
    if exp < datetime.___():  # Quelle méthode pour le temps actuel UTC ?
        raise ValueError("Token expiré")
    
    return payload


# Test
token = create_token({"sub": "alice@game.com", "role": "admin"})
print(f"\n🎫 Token: {token[:50]}...")
payload = decode_token(token)
print(f"📋 Payload: {payload}")


# ============================================================
# PARTIE 3 : Système d'auth complet
# ============================================================

class AuthService:
    def __init__(self):
        self.users: dict[str, dict] = {}
        self._next_id = 1
    
    def register(self, email: str, username: str, password: str) -> dict:
        """Inscrit un nouvel utilisateur."""
        if email ___ self.users:  # Quel opérateur pour "existe dans" ?
            raise ValueError("Email déjà utilisé")
        
        user = {
            "id": self._next_id,
            "email": email,
            "username": username,
            "hashed_password": hash_password(password),
            "role": "player",
        }
        self.users[email] = user
        self._next_id += 1
        return {"id": user["id"], "email": email, "username": username}
    
    def login(self, email: str, password: str) -> str:
        """Connecte un utilisateur et retourne un token."""
        user = self.users.___(email)  # Quelle méthode pour chercher sans erreur ?
        if user is None:
            ___ ValueError("Email inconnu")
        
        if not verify_password(password, user["hashed_password"]):
            raise ValueError("Mot de passe incorrect")
        
        return create_token({
            "sub": user["email"],
            "role": user["role"],
            "username": user["username"],
        })
    
    def get_current_user(self, token: str) -> dict:
        """Récupère l'utilisateur à partir du token."""
        ___:  # Quel bloc pour capturer les erreurs ?
            payload = decode_token(token)
        except ValueError as e:
            raise ValueError(f"Auth failed: {e}")
        
        email = payload.get("sub")
        if email not in self.users:
            raise ValueError("Utilisateur non trouvé")
        
        user = self.users[email]
        return {"id": user["id"], "email": email, "username": user["username"], "role": user["role"]}
    
    def require_role(self, token: str, role: str) -> dict:
        """Vérifie que l'utilisateur a le bon rôle."""
        user = self.get_current_user(token)
        if user["role"] != role:
            raise PermissionError(f"Rôle '{role}' requis, vous êtes '{user['role']}'")
        return user


# Test complet
auth = AuthService()

print("\n🎮 Test Auth Service:")
alice = auth.register("alice@game.com", "Alice", "password123")
print(f"  ✅ Register: {alice}")

token = auth.login("alice@game.com", "password123")
print(f"  ✅ Login: token={token[:30]}...")

user = auth.get_current_user(token)
print(f"  ✅ Current user: {user}")

try:
    auth.login("alice@game.com", "wrong_password")
except ValueError as e:
    print(f"  ❌ Wrong password: {e}")

try:
    auth.register("alice@game.com", "Alice2", "pass")
except ValueError as e:
    print(f"  ❌ Duplicate: {e}")

try:
    auth.require_role(token, "admin")
except PermissionError as e:
    print(f"  ❌ Role check: {e}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
