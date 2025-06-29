from fastapi import FastAPI
from contextlib import asynccontextmanager
from middleware.log_middleware import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("__FastAPI server is starting.")
    yield
    logger.info("__FastAPI server is shutting down.")