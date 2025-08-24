# exceptions.py


class ParserFindTagException(Exception):
    """Ошибка при поиске тега в HTML."""


class ParserRequestException(Exception):
    """Кастомное исключение для ошибок при запросе."""


class ParserSectionNotFound(Exception):
    """Не найден нужный раздел документации."""
