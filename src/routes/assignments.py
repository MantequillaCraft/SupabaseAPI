from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from utils import general, setup


router = APIRouter()


@router.get("/get_class")
async def get_class(
    class_id:str= Query(...)
):
    supabase = setup.supabase
    clases = (
        supabase.table("assignments")
        .select("*")
        .eq("id", class_id)
        .execute()
    )
    return JSONResponse(clases)

@router.get("/get_classes")
async def get_all_classes():
    try:
        supabase = setup.supabase
        clases = supabase.table("assignments").select("*").execute()
        
        return JSONResponse(clases.data)
    except Exception as e:
        return ( e )
    

@router.get("/add")
async def add_class(
    class_title:str= Query(...)
):
    try:
        supabase = setup.supabase
        clases = (
            supabase.table("assignments")
            .insert({
                "title" : class_title
            })
            .execute()
        )
        return JSONResponse(clases)
    except Exception as e:
        return JSONResponse ({
            "error" : f"Something went wrong {e}"
        })