# Тестовое задание к первому интенсиву

Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать
REST API по работе с меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет
приложена Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.
Даны 3 сущности: Меню, Подменю, Блюдо.
## Зависимости:
- У меню есть подменю, которые к ней привязаны.
- У подменю есть блюда.
## Условия:
- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
- Во время запуска тестового сценария БД должна быть пуста.

# Установка и запуск

- Скачать репозиторий проекта
```bash
git clone https://github.com/expmax85/Test_app.git
```

- Переместиться в корень проекта и установить зависимости:
```bash
cd Test_app
pip install -r requirements.txt
```

- Подключить базу данных, заполнить файл .env.

- Выполнить миграции командой:
```bash
alembic upgrade head
```

- Запустить проект командой:
 ```bash
uvicorn src.main:app --reload
```

# Docker
## Запуск приложения через докер
```bash
docker compose -f docker-compose.yml --env-file ./conf/.env.main build
docker compose -f docker-compose.yml --env-file ./conf/.env.main up -d
```

## Запуск приложения в режиме тестирования
```bash
docker compose -f docker-compose-test.yml --env-file ./conf/.env.test build
docker compose -f docker-compose-test.yml --env-file ./conf/.env.test up
```
