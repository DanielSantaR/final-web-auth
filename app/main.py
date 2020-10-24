import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router, prefix="/api")
    return application


app = create_application()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
