from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# =========================
# 🔐 "DATABASE" (demo)
# =========================
users_db = {
    "user1": {
        "api_key": "key-user-1",
        "enc_key": Fernet.generate_key().decode()
    },
    "user2": {
        "api_key": "key-user-2",
        "enc_key": Fernet.generate_key().decode()
    }
}


# =========================
# 📦 REQUEST MODEL
# =========================
class TextRequest(BaseModel):
    text: str


# =========================
# 🔍 API KEY AUTH
# =========================
def get_user(x_api_key: str = Header(None)):
    for username, data in users_db.items():
        if data["api_key"] == x_api_key:
            return username, data

    raise HTTPException(status_code=401, detail="Invalid API Key")


# =========================
# 🔐 ENCRYPT
# =========================
@app.post("/crypt")
def encrypt(req: TextRequest, user=Depends(get_user)):
    username, data = user

    cipher = Fernet(data["enc_key"].encode())
    encrypted = cipher.encrypt(req.text.encode()).decode()

    return {
        "user": username,
        "encrypted": encrypted
    }


# =========================
# 🔓 DECRYPT
# =========================
@app.post("/decrypt")
def decrypt(req: TextRequest, user=Depends(get_user)):
    username, data = user

    cipher = Fernet(data["enc_key"].encode())
    decrypted = cipher.decrypt(req.text.encode()).decode()

    return {
        "user": username,
        "decrypted": decrypted
    }