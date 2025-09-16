from fastapi import APIRouter, Query, HTTPException, Header
from fastapi.responses import JSONResponse
from src.utils import general, setup

router = APIRouter()


@router.get("/get_assignment")
async def get_assignment(
    class_id:str= Query(...)
):
    try:
        supabase = setup.supabase
        clases = (
            supabase.table("assignments")
            .select("*")
            .eq("id", class_id)
            .execute()
        )
        return JSONResponse(clases.data[0])
    except Exception as e:
        return JSONResponse (
            content={"error" : str(e)},
            status_code=500
        )


@router.get("/get_assignments")
async def get_all_assignments():
    try:
        supabase = setup.supabase
        clases = supabase.table("assignments").select("*").execute()
        
        return JSONResponse(clases.data)
    except Exception as e:
        return JSONResponse (
            content={"error" : str(e)},
            status_code=500
        )


@router.get("/add_assignment")
async def add_assignment(
    auth_token:str = Header(...),
    assignment_title:str= Query(...)
):
    general.authentication(auth_token=auth_token)

    try:
        supabase = setup.supabase
        clases = (
            supabase.table("assignments")
            .insert({
                "title" : assignment_title
            })
            .execute()
        )

        return JSONResponse({
            "message" : "Assignmente create Succesfully ",
            "assignment_id" : clases.data[0]["id"]
        })
    except Exception as e:
        return JSONResponse (
            content={"error" : str(e)},
            status_code=500
        )