from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.database import engine, get_db, actions
from src.models import schemas, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Menu
@app.post("/api/v1/menus", response_model=schemas.Menu)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = actions.menu_orm.create(db=db, obj_in=menu)
    result = actions.menu_orm.serialize(menu)
    return JSONResponse(result, status_code=201)


@app.get("/api/v1/menus", response_model=list[schemas.Menu])
def get_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = actions.menu_orm.get_all_with_relates(db=db, skip=skip, limit=limit)
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def get_menu(menu_id, db: Session = Depends(get_db)):
    menu = actions.menu_orm.get_with_relates(db=db, menu_id=menu_id)
    if not menu or not any(menu):
        raise HTTPException(detail="menu not found", status_code=404)
    return JSONResponse(actions.menu_orm.to_json(menu), status_code=200)


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id, menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    updated = actions.menu_orm.update(db=db, id_obj=menu_id, obj_data=menu)
    if not updated:
        raise HTTPException(detail="menu not found", status_code=200)
    menu = actions.menu_orm.get_with_relates(db=db, menu_id=menu_id)
    return JSONResponse(actions.menu_orm.to_json(menu), status_code=200)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    if not actions.menu_orm.check_exist(db=db, menu_id=menu_id):
        raise HTTPException(detail='menu not exists', status_code=404)
    actions.menu_orm.remove(db=db, id_obj=menu_id)
    return JSONResponse({'status': True, 'message': 'The menu has been deleted'}, status_code=200)


# SubMenu
@app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.SubMenu)
def create_submenu(menu_id: int, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    submenu = actions.submenu_orm.create(db=db, obj_in=submenu, menu_id=menu_id)
    result = actions.submenu_orm.serialize(submenu, exclude_fields=['menu_id', ])
    return JSONResponse(result, status_code=201)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = actions.submenu_orm.get_with_relates(db=db, submenu_id=submenu_id, menu_id=menu_id)
    if not submenu:
        raise HTTPException(detail="submenu not found", status_code=404)
    return JSONResponse(actions.submenu_orm.to_json(submenu), status_code=200)


@app.get('/api/v1/menus/{menu_id}/submenus', response_model=list[schemas.SubMenu])
def get_submenus(menu_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    submenus = actions.submenu_orm.get_all_with_relates(db=db, menu_id=menu_id, skip=skip, limit=limit)
    return submenus


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    if not actions.submenu_orm.check_exist_relates(db, submenu_id, menu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    actions.submenu_orm.remove(db=db, id_obj=submenu_id)
    return JSONResponse({'status': True, 'message': 'The submenu has been deleted'}, status_code=200)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
def update_submenu(menu_id: int, submenu_id: int, submenu: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    if not actions.submenu_orm.check_exist_relates(db, submenu_id, menu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    actions.submenu_orm.update(db=db, id_obj=submenu_id, obj_data=submenu)
    submenu = actions.submenu_orm.get_with_relates(db=db, submenu_id=submenu_id, menu_id=menu_id)
    return JSONResponse(actions.submenu_orm.to_json(submenu), status_code=200)


# Dish
@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish)
def create_dish(menu_id: int, submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    if not actions.submenu_orm.check_exist_relates(db, submenu_id, menu_id):
        raise HTTPException(detail="submenu for not found", status_code=404)
    dish = actions.dish_orm.create(db=db, obj_in=dish, submenu_id=submenu_id)
    result = actions.dish_orm.serialize(dish, exclude_fields=['submenu_id', ])
    return JSONResponse(result, status_code=201)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    if not actions.dish_orm.check_exist_relates(db=db, dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id):
        raise HTTPException(detail="dish not found", status_code=404)
    actions.dish_orm.remove(db=db, id_obj=dish_id)
    return JSONResponse({'status': True, 'message': 'The dish has been deleted'}, status_code=200)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
def get_dishes(menu_id: int, submenu_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return actions.dish_orm.get_all_with_relates(db=db, menu_id=menu_id, submenu_id=submenu_id, skip=skip, limit=limit)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = actions.dish_orm.get_with_relates(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if not dish:
        raise HTTPException(detail="dish not found", status_code=404)
    result = actions.dish_orm.serialize(dish, exclude_fields=['submenu_id', ])
    return JSONResponse(result, status_code=200)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    if not actions.dish_orm.check_exist_relates(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id):
        raise HTTPException(detail="dish not found", status_code=404)
    actions.dish_orm.update(db=db, id_obj=dish_id, obj_data=dish)
    dish = actions.dish_orm.get_with_relates(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    return JSONResponse(actions.dish_orm.to_json(dish), status_code=200)
