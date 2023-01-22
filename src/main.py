from fastapi import FastAPI
from sqlalchemy.exc import StatementError
from starlette.responses import JSONResponse

from src.config import settings
from src.routes import menus, submenus, dishes

app = FastAPI(debug=settings.DEBUG)

app.include_router(menus.router, prefix='/api/v1')
app.include_router(submenus.router, prefix='/api/v1')
app.include_router(dishes.router, prefix='/api/v1')


@app.exception_handler(StatementError)
async def validation_exception_handler(request, exc: StatementError):
    return JSONResponse({"detail": "incorrect data"}, status_code=404)
