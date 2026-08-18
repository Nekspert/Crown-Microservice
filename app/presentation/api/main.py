import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import config
from .v1.routes import tender
from ...infrastructure.broker.redis import build_async_redis_manager
from ...infrastructure.db.database import build_async_db_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application lifespan")

    db = build_async_db_manager(config.db.postgresql)
    broker = build_async_redis_manager(config.broker.redis)
    app.state.manager = db
    app.state.broker = broker

    await db.connect()
    await broker.connect()

    try:
        yield
    finally:
        await broker.close()
        await db.close()

    logger.info("Application lifespan stopped")


def create_app() -> FastAPI:
    logger.info("Creating FastAPI application")

    app = FastAPI(
        title=config.project.project_title,
        description=config.project.project_description,
        lifespan=lifespan,
    )

    logger.info("Registering middlewares")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors.cors_allow_origins,
        allow_headers=config.cors.cors_allow_headers,
        allow_methods=config.cors.cors_allow_methods,
        allow_credentials=config.cors.cors_allow_credentials,
    )

    logger.info("Registering error handlers")

    @app.exception_handler(KeyError)
    async def not_found_handler(request: Request, exc: KeyError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ValueError)
    async def bad_request_handler(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    logger.info("Registering routers")

    app.include_router(tender.router, prefix=config.api.prefix)

    return app


main_app = create_app()
