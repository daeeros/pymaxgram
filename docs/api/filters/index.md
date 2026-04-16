# Фильтры

Экспортируемые из `maxgram.filters`:

- `Filter` — базовый класс
- `Command` — фильтр текстовых команд
- `CommandObject` — результат парсинга команды
- `CallbackData` — структурированные callback данные
- `StateFilter` — фильтр FSM-состояния
- `ExceptionTypeFilter` — фильтр по типу исключения
- `ExceptionMessageFilter` — фильтр по тексту ошибки
- `MagicData` — фильтр по данным middleware
- `and_f`, `or_f`, `invert_f` — логические комбинаторы
