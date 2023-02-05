from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import settings
from src.routes import dishes, menus, submenus, tasks

app = FastAPI(
    debug=settings.App.DEBUG,
    title=settings.App.TITLE,
    description=settings.App.DESCRIPTION,
    version=settings.App.VERSION,
)


app.include_router(menus.router, prefix=settings.App.PREFIX)
app.include_router(submenus.router, prefix=settings.App.PREFIX)
app.include_router(dishes.router, prefix=settings.App.PREFIX)
app.include_router(tasks.router, prefix=settings.App.PREFIX)

app.mount("/uploads", StaticFiles(directory="uploads"))
