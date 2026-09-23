# Установка

pymaxgram больше не публикуется на PyPI --- ставится напрямую из GitHub.
Каждый релиз помечен тегом `vX.Y.Z` (список: [теги](https://github.com/daeeros/pymaxgram/tags)).

## Через pip

```bash
pip install "pymaxgram @ git+https://github.com/daeeros/pymaxgram.git@v4.0.47"
```

С дополнительными зависимостями (extras):

```bash
pip install "pymaxgram[fastapi] @ git+https://github.com/daeeros/pymaxgram.git@v4.0.47"
```

## В requirements.txt

```text
pymaxgram[fastapi] @ git+https://github.com/daeeros/pymaxgram.git@v4.0.47
```

Всегда указывайте тег, а не ветку: так на всех серверах стоит одна и та же
версия. Обновление --- поменять тег и выполнить `pip install -r requirements.txt`.

!!! note "Нужен git"
    pip клонирует репозиторий и собирает пакет сам, поэтому на машине должен
    быть установлен `git`.

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
