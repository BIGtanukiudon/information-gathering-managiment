from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.config import DATABASE_URL
from databases import Database
from routers import collection_destination

database = Database(DATABASE_URL, min_size=2, max_size=5)


def get_application():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(collection_destination.router)

    return app


app = get_application()


@app.on_event("startup")
async def startup():
    try:
        await database.connect()
    except Exception as e:
        print(e)


@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
    except Exception as e:
        print(e)


@app.get("/")
async def root():
    return {"message": "Hello apis test."}
