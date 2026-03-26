"""Module 18 — Solution exercice à trou #2"""

from fastapi import FastAPI
import sentry_sdk

sentry_sdk.init(
    dsn="https://fake_key@o22222.ingest.sentry.io/44444",
    traces_sample_rate=0.1,
    environment="production"
)

app = FastAPI()

@app.get("/acheter-epee")
def fake_crash():
    item = "Epée de feu"
    is_admin = False
    
    raise ValueError("Le solde du joueur est insuffisant !")
    
    return {"msg": "Acheté"}
