====================
Информация о боте
====================

GetMe
-----

``GET /me`` → ``BotInfo``

Получает информацию о текущем боте.

.. code-block:: python

   class GetMe(MaxMethod[BotInfo]):
       pass  # Нет параметров

Возвращает ``BotInfo`` со всеми полями: ``user_id``, ``first_name``, ``username``,
``avatar_url``, ``commands`` и т.д.

Пример
------

.. code-block:: python

   info = await bot.get_me()
   print(f"Bot: {info.first_name} (@{info.username})")
   print(f"ID: {info.user_id}")
   if info.commands:
       for cmd in info.commands:
           print(f"  /{cmd.name} — {cmd.description}")

Исходный файл
--------------

``maxgram/methods/get_me.py``
