from fastapi import FastAPI
from starlette import status

from src.config import settings
from src.database.init_data_db import init_test_data_db
from src.models import schemas
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


@app.get(
    "/generate",
    response_model=schemas.SuccessInit,
    status_code=status.HTTP_200_OK,
    tags=["Generate data"],
)
async def generate_test_data():
    """
    Service route for generating test menus, submenus and dishes data
    """
    await init_test_data_db()
    return {"status": True, "message": "All data was created"}
