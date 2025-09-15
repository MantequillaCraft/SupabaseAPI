import jwt
import os
from dotenv import load_dotenv
from .setup import supabase
from fastapi import HTTPException
from fastapi.responses import JSONResponse

load_dotenv()


def authentication(auth_token: str):
    try:
        decoded = jwt.decode(auth_token, key=os.getenv("SECRET"), algorithms=os.getenv("ALGORITHM"))

        user = (
            supabase.table("profiles")
            .select("*")
            .eq("id", decoded["id"])
            .eq("email", decoded["email"])
            .execute()
        )

        return user.data[0], decoded
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
