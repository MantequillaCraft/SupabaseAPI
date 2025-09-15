from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from schemas import request_schemas
from utils import setup, general
import jwt
from datetime import datetime, timedelta, timezone
import os 
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/sign_up")
async def sign_up( req : request_schemas.SignUpRequest):
    try:
        supabase = setup.supabase

        auth = supabase.auth.sign_up(
            {
                "email" : req.email, "password" : req.password
            }
        )
        user_id = auth.user.id
        print(user_id)

        response = (
            supabase.table("profiles")
            .insert(
                {
                    "id": user_id,
                    "email" : req.email,
                    "name" : req.name
                }
            )
            .execute()
        )

        return JSONResponse({
            "message" : "User has been SingUp succesfully",
            "data" : {
                "userId" : user_id,
                "userName" : req.name
            }
        })
    except Exception as e:
        return JSONResponse(
            {"mesage" : f"Something went wrong : {e}"},
            status_code=500
        )


@router.get("/get_token")
async def acces_token(
    user_id = Header(...)
):
    try:
        supabase = setup.supabase
        response = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=401, detail="User not found")

        user_email =  response.data[0]["email"]

        payload = {
            "id": user_id,
            "email" : user_email,
            "iat": int(datetime.now(timezone.utc).timestamp()),                          # emitido en
            "nbf": int(datetime.now(timezone.utc).timestamp()),                          # no válido antes de
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp()),  # expira en 1h
        }

        encoder_jwt = jwt.encode( payload=payload, key=os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM") )

        return JSONResponse({
            "auth_token" : encoder_jwt,
            "message" : "token generates succesfully"
        })

    except Exception as e:
        return JSONResponse(
            {"mesage" : f"Something went wrong : {e}"},
            status_code=500
        )

@router.get("/get_userdata")
async def decode_token(
    auth_token: str = Header(...)
):
    user_data, decoded  = general.authentication(auth_token=auth_token)
    return JSONResponse({
        "payload" : decoded,
        "user_data" : user_data
    })