# Исключения

## Иерархия

```text
MaxgramError
├── DetailedMaxgramError
│   ├── MaxAPIError
│   │   ├── MaxNetworkError
│   │   ├── MaxBadRequest              (400)
│   │   ├── MaxUnauthorizedError       (401)
│   │   ├── MaxForbiddenError          (403)
│   │   ├── MaxNotFound                (404)
│   │   ├── MaxConflictError           (409)
│   │   ├── MaxRateLimitError          (429)
│   │   ├── MaxServerError             (5xx)
│   │   │   └── MaxServiceUnavailable  (503)
│   │   └── ClientDecodeError
│   ├── DataNotDictLikeError
│   └── UnsupportedKeywordArgument
└── ClientDecodeError
```

## Описание

### MaxgramError

Базовое исключение фреймворка.

### DetailedMaxgramError

```python
class DetailedMaxgramError(MaxgramError):
    url: str | None = None
    message: str
```

### MaxAPIError

```python
class MaxAPIError(DetailedMaxgramError):
    method: MaxMethod    # Метод, вызвавший ошибку
    message: str         # Сообщение об ошибке
    label: str | None    # Метка ошибки
```

### HTTP-ошибки

| Исключение | Код | Когда возникает |
| --- | --- | --- |
| `MaxBadRequest` | 400 | Некорректные параметры запроса |
| `MaxUnauthorizedError` | 401 | Недействительный или отсутствующий токен |
| `MaxForbiddenError` | 403 | Нет прав на операцию |
| `MaxNotFound` | 404 | Чат, пользователь или сообщение не найдены |
| `MaxConflictError` | 409 | Конфликт (дублирование операции) |
| `MaxRateLimitError` | 429 | Превышен лимит запросов к API |
| `MaxServerError` | 5xx | Внутренняя ошибка сервера MAX |
| `MaxServiceUnavailable` | 503 | Сервис временно недоступен |

### Другие исключения

- `MaxNetworkError` — сетевая ошибка (таймаут, разрыв соединения)
- `ClientDecodeError` — ошибка декодирования ответа
- `DataNotDictLikeError` — данные не являются словарём
- `UnsupportedKeywordArgument` — неподдерживаемый аргумент

## Исходный файл

`maxgram/exceptions.py`
