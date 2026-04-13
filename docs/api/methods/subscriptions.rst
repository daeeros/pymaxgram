============
Подписки
============

GetSubscriptions
----------------

``GET /subscriptions`` → ``list[Subscription]``

.. code-block:: python

   class GetSubscriptions(MaxMethod[list[Subscription]]):
       pass  # Нет параметров

CreateSubscription
------------------

``POST /subscriptions`` → ``bool``

.. code-block:: python

   class CreateSubscription(MaxMethod[bool]):
       url: str
       update_types: list[str] | None = None
       secret: str | None = None

Поля:

- **url** — URL вашего webhook-сервера
- **update_types** — типы обновлений (``["message_created", "message_callback", "bot_started"]``)
- **secret** — секретный токен для верификации запросов

DeleteSubscription
------------------

``DELETE /subscriptions`` → ``bool``

.. code-block:: python

   class DeleteSubscription(MaxMethod[bool]):
       url: str

Исходные файлы
--------------

- ``maxgram/methods/get_subscriptions.py``
- ``maxgram/methods/create_subscription.py``
- ``maxgram/methods/delete_subscription.py``
