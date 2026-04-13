===========
Вложения
===========

.. module:: maxgram.types.attachment

Типы вложений (Attachment)
--------------------------

Attachment (базовый)
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Attachment(MaxObject):
       type: str
       payload: Any | None = None

Подтипы
^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Класс
     - type
     - Описание
   * - ``PhotoAttachment``
     - ``"image"``
     - Изображение
   * - ``VideoAttachment``
     - ``"video"``
     - Видео
   * - ``AudioAttachment``
     - ``"audio"``
     - Аудио
   * - ``FileAttachment``
     - ``"file"``
     - Файл
   * - ``StickerAttachment``
     - ``"sticker"``
     - Стикер
   * - ``ContactAttachment``
     - ``"contact"``
     - Контакт
   * - ``InlineKeyboardAttachment``
     - ``"inline_keyboard"``
     - Inline-клавиатура
   * - ``LocationAttachment``
     - ``"location"``
     - Геолокация
   * - ``ShareAttachment``
     - ``"share"``
     - Поделиться

Все подтипы наследуют от ``Attachment`` и устанавливают значение ``type`` по умолчанию.

Запросы вложений (AttachmentRequest)
-------------------------------------

.. module:: maxgram.types.attachment_request

Используются при отправке сообщений.

AttachmentRequest (базовый)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class AttachmentRequest(MaxObject):
       type: str
       payload: Any | None = None

Подтипы
^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Класс
     - type
     - Описание
   * - ``PhotoAttachmentRequest``
     - ``"image"``
     - Отправка изображения
   * - ``VideoAttachmentRequest``
     - ``"video"``
     - Отправка видео
   * - ``AudioAttachmentRequest``
     - ``"audio"``
     - Отправка аудио
   * - ``FileAttachmentRequest``
     - ``"file"``
     - Отправка файла
   * - ``InlineKeyboardAttachmentRequest``
     - ``"inline_keyboard"``
     - Отправка клавиатуры

InlineKeyboardAttachmentRequest
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Дополнительный метод класса:

.. code-block:: python

   @classmethod
   def from_buttons(
       cls,
       buttons: list[list[Button]],
   ) -> InlineKeyboardAttachmentRequest

Создаёт вложение клавиатуры из двумерного списка кнопок.

Пример отправки вложений
-------------------------

.. code-block:: python

   from maxgram.types import Attachment

   # Inline-клавиатура
   await message.answer(
       text="Choose:",
       attachments=[
           Attachment(
               type="inline_keyboard",
               payload=keyboard.model_dump(mode="json"),
           ),
       ],
   )

   # Изображение по токену
   await message.answer(
       text="Photo:",
       attachments=[
           Attachment(type="image", payload={"token": "abc123"}),
       ],
   )

Исходные файлы
--------------

- ``maxgram/types/attachment.py``
- ``maxgram/types/attachment_request.py``
