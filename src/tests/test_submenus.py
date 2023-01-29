import pytest

from src.tests import menu_orm
from src.tests import submenu_orm


@pytest.mark.asyncio
async def test_create_submenu(test_app):
    menu = await menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    response = await test_app.post(
        f'api/v1/menus/{menu.id}/submenus/',
        json={'title': 'Test submenu 1', 'description': 'Test submenu descr 1'},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['title'] == 'Test submenu 1'
    assert 'id' in data
    await menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_get_submenu(test_app):
    menu = await menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await submenu_orm.create(
        {'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
        menu_id=menu.id,
    )
    response = await test_app.get(f'/api/v1/menus/{menu.id}/submenus/{submenu.id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == submenu.title
    assert data['id'] == str(submenu.id)
    await menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_get_submenus(test_app):
    menu = await menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    await submenu_orm.create(
        {'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
        menu_id=menu.id,
    )
    response = await test_app.get(f'/api/v1/menus/{menu.id}/submenus/')
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    await menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_update_menu(test_app):
    menu = await menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await submenu_orm.create(
        {'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
        menu_id=menu.id,
    )
    response = await test_app.patch(
        f'/api/v1/menus/{menu.id}/submenus/{submenu.id}',
        json={'title': 'Updated submenu 1', 'description': 'Updated submenu descr 1'},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] != submenu.title
    assert data['title'] == 'Updated submenu 1'
    assert data['id'] == str(submenu.id)
    await menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_delete_submenu(test_app):
    menu = await menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await submenu_orm.create(
        {'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
        menu_id=menu.id,
    )
    response = await test_app.delete(
        f'api/v1/menus/{menu.id}/submenus/{submenu.id}',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['status'] is True
    assert data['message'] == 'The submenu has been deleted'
    await menu_orm.remove(menu.id)
