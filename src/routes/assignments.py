from fastapi import APIRouter, Query, HTTPException, Header
from fastapi.responses import JSONResponse
from src.utils import general, setup

router = APIRouter()


@router.get("/get_assignment")
async def get_assignment(
    assignment_id:str= Query(...)
):
    try:
        supabase = setup.supabase
        clases = (
            supabase.table("assignments")
            .select("*")
            .eq("id", assignment_id)
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
        assignments = supabase.table("assignments").select("*", count="exact").execute()

        return JSONResponse({ "data" : { "total" : assignments.count },"something":assignments.data})
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
    user_data, _ = general.authentication(auth_token=auth_token)
    code = general.sanitize_string(text=assignment_title)
    try:
        supabase = setup.supabase
        clases = (
            supabase.table("assignments")
            .insert({
                "code" : code,
                "title" : assignment_title,
                "created_by" : user_data["id"]
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


@router.delete("/delete_assignment")
async def delete_assignment(
    auth_token:str = Header(...),
    assignment_id:str= Query(...)
):
    user_data, _ = general.authentication(auth_token=auth_token)
    try:
        supabase = setup.supabase
        a = (
            supabase.table("assignments")
            .select("title","created_by")
            .eq("id", assignment_id)
            .execute()
        )

        if user_data["id"] == a.data[0]["created_by"] or user_data["role"]=="admin":
            response = (
                supabase.table("assignments")
                .delete()
                .eq("id", assignment_id)
                .execute()
            )

            return JSONResponse({
                "message" : "Assignmente deleted Succesfully ",
                "assignment" : a.data[0]["title"]
            })
        else:
            return HTTPException(status_code=401, detail="Error, you have no permissions")
        
    except Exception as e:
        return JSONResponse (
            content={"error" : str(e)},
            status_code=500
        )