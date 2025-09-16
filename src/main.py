from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        {
            "message" : "Welcome to your FastAPI API :))"
        }
    )


from routes.auth import router as auth_router
from routes.assignments import router as assignments_router

app.include_router(auth_router, prefix="/auth", tags=["Authenticate"])
app.include_router(assignments_router, prefix="/class", tags=["Class"])