from fastapi import FastAPI
from sqlalchemy.exc import StatementError
from starlette.responses import JSONResponse
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
from src.config import settings
from src.routes import menus, submenus, dishes

app = FastAPI(debug=settings.DEBUG)

app.include_router(menus.router, prefix='/api/v1')
app.include_router(submenus.router, prefix='/api/v1')
app.include_router(dishes.router, prefix='/api/v1')


@app.exception_handler(StatementError)
async def validation_exception_handler(request, exc: StatementError):
    return JSONResponse({"detail": "incorrect data"}, status_code=404)


# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")