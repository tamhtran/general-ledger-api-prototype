import logging

from fastapi import FastAPI
from app.api import ping, balance, account, region
from app.db import init_db

log = logging.getLogger("uvicorn")

tags_metadata = [
    {
        "name": "balance",
        "description": "Operations related to balance calculations. This includes getting balance information based on account, date, and region.",

    },
    {
        "name": "account",
        "description": "Manage account data. Operations include retrieving account details.",
    },
    {
        "name": "region",
        "description": "Manage Region data. Operations include retrieving region details.",
    },
]



def create_application() -> FastAPI:
    application = FastAPI(openapi_tags=tags_metadata)
    # application.include_router(ping.router)
    application.include_router(balance.router, prefix="/balance", tags=["balance"])
    application.include_router(account.router, prefix="/account", tags=["account"])
    application.include_router(region.router, prefix="/region", tags=["region"])
    return application


app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")