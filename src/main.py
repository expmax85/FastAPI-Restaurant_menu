from fastapi import FastAPI

from src.database import engine
from src.models import Base
from src.routes import menus, submenus, dishes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)
