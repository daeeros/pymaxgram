# Установка

## Из PyPI

Самый простой способ установки --- через pip:

```bash
pip install pymaxgram
```

## Конкретная версия

```bash
pip install pymaxgram==4.0.1
```

## Из исходного кода

```bash
git clone https://github.com/daeeros/pymaxgram.git
cd pymaxgram
pip install .
```

## Для разработки

```bash
git clone https://github.com/daeeros/pymaxgram.git
cd pymaxgram
pip install -e .
```

## Зависимости

pymaxgram автоматически установит следующие зависимости:

| Пакет | Версия | Описание |
| --- | --- | --- |
| `aiohttp` | >= 3.9.0, < 3.14 | Асинхронный HTTP-клиент для запросов к API |
| `pydantic` | >= 2.4.1, < 2.13 | Валидация данных и типизированные модели |
| `magic-filter` | >= 1.0.12, < 1.1 | Декларативная фильтрация через объект `F` |
| `aiofiles` | >= 23.2.1, < 26.0 | Асинхронное чтение/запись файлов |
| `certifi` | >= 2023.7.22 | Корневые SSL-сертификаты |
| `typing-extensions` | >= 4.7.0, <= 5.0 | Расширения типизации Python |

## Проверка установки

```python
import maxgram
print(maxgram.__version__)  # 4.0.1
print(maxgram.__api_version__)  # 1.0
```

## Дополнительные зависимости

Для работы с прокси-серверами:

```bash
pip install aiohttp-socks
```

Для webhook-режима (если ещё не установлен aiohttp):

```bash
pip install aiohttp
```
