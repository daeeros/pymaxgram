============
Обработчики
============

Обработчики (handlers) — это async-функции или классы, реагирующие на события.

Функциональные обработчики
--------------------------

Самый распространённый способ — декораторы роутера:

.. code-block:: python

   from maxgram import Router

   router = Router()

   @router.message()
   async def handle_message(message, bot):
       await message.answer(text=message.body.text)

   @router.message_callback()
   async def handle_callback(callback, bot):
       await callback.answer(notification="OK")

   @router.bot_started()
   async def handle_start(event, bot):
       pass

   @router.error()
   async def handle_error(error, bot):
       pass

Инъекция зависимостей
---------------------

Обработчики получают аргументы через механизм инъекции на основе имён параметров:

.. code-block:: python

   @router.message()
   async def handler(
       message,          # Объект Message (событие)
       bot,              # Экземпляр Bot
       state,            # FSMContext (если FSM включён)
       raw_state,        # Строковое значение текущего состояния
       event_from_user,  # User — отправитель
       event_chat,       # Chat ID
       event_update,     # Исходный Update
       event_router,     # Router, обработавший событие
       dispatcher,       # Dispatcher
       # Любые данные из workflow_data и middleware
   ):
       pass

.. note::

   Вы можете указывать только те параметры, которые вам нужны. Остальные будут
   проигнорированы.

Данные из фильтров
^^^^^^^^^^^^^^^^^^

Фильтры могут возвращать словарь, данные из которого становятся доступны в обработчике:

.. code-block:: python

   from maxgram.filters import Command, CommandObject

   @router.message(Command("echo"))
   async def echo_cmd(message, command: CommandObject, bot):
       # command инъектирован фильтром Command
       if command.args:
           await message.answer(text=command.args)

Классовые обработчики
---------------------

Для сложных обработчиков можно использовать классы, наследуя от базовых:

BaseHandler
^^^^^^^^^^^

.. code-block:: python

   from maxgram.handlers import BaseHandler

   class BaseHandler[T]:
       event: T                   # Событие
       data: dict[str, Any]       # Данные middleware

       @property
       def bot(self) -> Bot: ...  # Экземпляр Bot

       @property
       def update(self) -> Update: ...  # Исходный Update

       @abstractmethod
       async def handle(self) -> Any: ...

MessageHandler
^^^^^^^^^^^^^^

.. code-block:: python

   from maxgram.handlers import MessageHandler

   class MyHandler(MessageHandler):
       async def handle(self):
           name = self.from_user.first_name if self.from_user else "Unknown"
           await self.event.answer(text=f"Hello, {name}!")

   # Регистрация
   router.message.register(MyHandler)

Свойства:

- ``from_user`` → ``User | None`` — отправитель (``message.sender``)
- ``chat_id`` → ``int | None`` — ID чата (``message.recipient.chat_id``)

CallbackHandler
^^^^^^^^^^^^^^^

.. code-block:: python

   from maxgram.handlers import CallbackHandler

   class MyCallback(CallbackHandler):
       async def handle(self):
           await self.event.answer(notification="Handled!")

Свойства:

- ``from_user`` → ``User`` — пользователь, нажавший кнопку
- ``message`` → ``Message | None`` — сообщение, к которому была прикреплена кнопка

BotStartedHandler
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from maxgram.handlers import BotStartedHandler

   class WelcomeHandler(BotStartedHandler):
       async def handle(self):
           pass

Свойства:

- ``from_user`` → ``User | None``
- ``chat_id`` → ``int | None``

ErrorHandler
^^^^^^^^^^^^

.. code-block:: python

   from maxgram.handlers import ErrorHandler

   class MyErrorHandler(ErrorHandler):
       async def handle(self):
           print(f"Error: {self.exception_name}: {self.exception_message}")

Свойства:

- ``exception_name`` → ``str`` — имя класса исключения
- ``exception_message`` → ``str`` — текст исключения

MessageHandlerCommandMixin
^^^^^^^^^^^^^^^^^^^^^^^^^^

Миксин для доступа к данным команды:

.. code-block:: python

   from maxgram.handlers import MessageHandler, MessageHandlerCommandMixin

   class CommandHandler(MessageHandlerCommandMixin, MessageHandler):
       async def handle(self):
           if self.command and self.command.args:
               await self.event.answer(text=f"Args: {self.command.args}")

Свойство:

- ``command`` → ``CommandObject | None``

Регистрация классовых обработчиков
----------------------------------

.. code-block:: python

   from maxgram.filters import Command

   # Через register()
   router.message.register(MyHandler, Command("test"))

   # Через декоратор
   @router.message(Command("test"))
   class MyHandler(MessageHandler):
       async def handle(self):
           pass
