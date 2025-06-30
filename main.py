from fastapi import FastAPI
from routers import users, tasks, admin
from database import engine
from models import Base
from middleware.log_middleware import LoggerMiddleware
from middleware.rate_limiter import RedisRateLimiter
from middleware.log_events import lifespan
from middleware.cors import add_cors_middleware

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

add_cors_middleware(app)

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(admin.router)

app.add_middleware(LoggerMiddleware)
app.add_middleware(RedisRateLimiter)