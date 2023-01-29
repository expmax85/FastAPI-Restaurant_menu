from fastapi import FastAPI

from src.config import settings
from src.routes import dishes
from src.routes import menus
from src.routes import submenus

app = FastAPI(debug=settings.DEBUG,
              title='YLab RestMenu',
              description='Test API application',
              version='3.0')

app.include_router(menus.router, prefix='/api/v1')
app.include_router(submenus.router, prefix='/api/v1')
app.include_router(dishes.router, prefix='/api/v1')
