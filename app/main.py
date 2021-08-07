from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import collection_destination, content, authentication


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
    app.include_router(content.router)
    app.include_router(authentication.router)

    return app


app = get_application()
