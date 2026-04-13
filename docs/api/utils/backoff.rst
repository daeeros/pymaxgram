=========
Backoff
=========

.. module:: maxgram.utils.backoff

Экспоненциальный backoff для повторных попыток.

BackoffConfig
-------------

.. code-block:: python

   @dataclass
   class BackoffConfig:
       min_delay: float = 1.0    # Минимальная задержка
       max_delay: float = 5.0    # Максимальная задержка
       factor: float = 1.3       # Множитель
       jitter: float = 0.1       # Дисперсия (нормальное распределение)

Backoff
-------

.. code-block:: python

   class Backoff:
       def __init__(self, config: BackoffConfig = BackoffConfig()) -> None: ...

       counter: int               # Количество попыток
       next_delay: float          # Следующая задержка

       def reset(self) -> None    # Сбросить счётчик
       async def asleep(self) -> None  # Async sleep с текущей задержкой
       def __next__(self) -> float     # Получить следующую задержку

Используется ``Dispatcher._listen_updates()`` для повторных попыток
при сбоях подключения.

Исходный файл
--------------

``maxgram/utils/backoff.py``
