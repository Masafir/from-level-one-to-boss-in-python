"""Module 09 — Solution exercice à trou #1"""

from datetime import datetime, timedelta
from passlib.context import CryptContext
import json, base64, hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(plain: str, hashed: str) -> bool: return pwd_context.verify(plain, hashed)

password = "super_secret_123"
hashed = hash_password(password)
print(f"🔒 Hash: {hashed[:30]}...")
print(f"✅ Verify correct: {verify_password(password, hashed)}")
print(f"❌ Verify wrong: {verify_password('wrong', hashed)}")

SECRET_KEY = "my-super-secret-key"

def create_token(data: dict, expires_minutes: int = 30) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload["exp"] = expire.isoformat()
    payload_json = json.dumps(payload)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode()
    signature = hashlib.sha256(f"{payload_b64}.{SECRET_KEY}".encode()).hexdigest()[:32]
    return f"{payload_b64}.{signature}"

def decode_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 2: raise ValueError("Token malformé")
    payload_b64, signature = parts
    expected_sig = hashlib.sha256(f"{payload_b64}.{SECRET_KEY}".encode()).hexdigest()[:32]
    if signature != expected_sig: raise ValueError("Signature invalide")
    payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode())
    exp = datetime.fromisoformat(payload["exp"])
    if exp < datetime.utcnow(): raise ValueError("Token expiré")
    return payload

token = create_token({"sub": "alice@game.com", "role": "admin"})
print(f"\n🎫 Token: {token[:50]}...")
payload = decode_token(token)
print(f"📋 Payload: {payload}")

class AuthService:
    def __init__(self):
        self.users: dict[str, dict] = {}
        self._next_id = 1

    def register(self, email: str, username: str, password: str) -> dict:
        if email in self.users: raise ValueError("Email déjà utilisé")
        user = {"id": self._next_id, "email": email, "username": username,
                "hashed_password": hash_password(password), "role": "player"}
        self.users[email] = user; self._next_id += 1
        return {"id": user["id"], "email": email, "username": username}

    def login(self, email: str, password: str) -> str:
        user = self.users.get(email)
        if user is None: raise ValueError("Email inconnu")
        if not verify_password(password, user["hashed_password"]): raise ValueError("Mot de passe incorrect")
        return create_token({"sub": user["email"], "role": user["role"], "username": user["username"]})

    def get_current_user(self, token: str) -> dict:
        try: payload = decode_token(token)
        except ValueError as e: raise ValueError(f"Auth failed: {e}")
        email = payload.get("sub")
        if email not in self.users: raise ValueError("Utilisateur non trouvé")
        user = self.users[email]
        return {"id": user["id"], "email": email, "username": user["username"], "role": user["role"]}

    def require_role(self, token: str, role: str) -> dict:
        user = self.get_current_user(token)
        if user["role"] != role: raise PermissionError(f"Rôle '{role}' requis")
        return user

auth = AuthService()
print("\n🎮 Test Auth Service:")
alice = auth.register("alice@game.com", "Alice", "password123")
print(f"  ✅ Register: {alice}")
token = auth.login("alice@game.com", "password123")
print(f"  ✅ Login: token={token[:30]}...")
user = auth.get_current_user(token)
print(f"  ✅ Current user: {user}")
try: auth.login("alice@game.com", "wrong")
except ValueError as e: print(f"  ❌ Wrong password: {e}")
try: auth.register("alice@game.com", "Alice2", "pass")
except ValueError as e: print(f"  ❌ Duplicate: {e}")
try: auth.require_role(token, "admin")
except PermissionError as e: print(f"  ❌ Role check: {e}")
print("\n✅ Exercice terminé avec succès !")
