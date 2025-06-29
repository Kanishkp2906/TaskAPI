from fastapi import FastAPI
from routers import users, tasks, admin
from database import engine
from models import Base
from middleware.log_middleware import LoggerMiddleware
from middleware.log_events import lifespan

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(admin.router)

app.add_middleware(LoggerMiddleware)