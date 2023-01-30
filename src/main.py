from fastapi import FastAPI

from src.config import settings
from src.routes import dishes
from src.routes import menus
from src.routes import submenus

app = FastAPI(debug=settings.App.DEBUG,
              title=settings.App.TITLE,
              description=settings.App.DESCRIPTION,
              version=settings.App.VERSION)

app.include_router(menus.router, prefix=settings.App.PREFIX)
app.include_router(submenus.router, prefix=settings.App.PREFIX)
app.include_router(dishes.router, prefix=settings.App.PREFIX)
