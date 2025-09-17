import jwt
import os
import re
from dotenv import load_dotenv
from src.utils.setup import supabase
from fastapi import HTTPException

load_dotenv()

def enconde(payload: dict):
    return jwt.encode( payload=payload, key=os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM") )


def authentication(auth_token: str):
    try:
        decoded = jwt.decode(auth_token, key=os.getenv("SECRET"), algorithms=os.getenv("ALGORITHM"))

        user = (
            supabase.table("users")
            .select("*")
            .eq("id", decoded["id"])
            .eq("email", decoded["email"])
            .execute()
        )

        return user.data[0], decoded #user.data[0] = data del usuario, decoded = payload decoded
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


def sanitize_string(text: str) -> str:
    # Reemplaza cualquier cosa que NO sea a-z, A-Z, 0-9 por "_"
    sanitized = re.sub(r'[^a-zA-Z0-9]', '_', text)

    # Convierte todo a minúsculas
    return sanitized.lower()
