from fastapi import FastAPI

from src.routes import menus, submenus, dishes

app = FastAPI(debug=True)

app.include_router(menus.router, prefix='/api/v1')
app.include_router(submenus.router, prefix='/api/v1')
app.include_router(dishes.router, prefix='/api/v1')
