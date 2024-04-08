## Запуск локально:

1. Установи переменные среды (.env-examle). Выстави DEV=True.
2. Первый терминал:
```
python src/manage.py migrate
```
```
python src/manage.py runserver
```
3. Второй терминал:
```
python bot/bot_sync.py
```
4. Третий терминал:
```
python sender
```

TODO
[ ] Сделать проверку на на то, что в БД нет заказов со статусами "New" и "Approved", которые имеют desired_departure > today.
