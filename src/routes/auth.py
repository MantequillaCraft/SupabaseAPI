from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.schemas import request_schemas
from src.utils import setup, general
from datetime import datetime, timedelta, timezone
import jwt


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

        response = (
            supabase.table("users")
            .insert(
                {
                    "id" : user_id,
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
        return ( e )


@router.get("/get_token")
async def acces_token(
    user_email = Header(...),
    user_password = Header(...)
):
    try:
        supabase = setup.supabase
        user = supabase.auth.sign_in_with_password(
            {
                "email" : user_email,
                "password" : user_password
            }
        )

        user_data = dict(user)
        return JSONResponse(content={
            "token" : user.session.access_token,
            "data" : jsonable_encoder(user_data)
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
    user_data, user_id  = general.authentication(auth_token=auth_token)
    return JSONResponse({
        "user_data" : user_data,
        "user_id" : user_id,
    })