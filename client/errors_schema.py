"""Pydantic-схемы ответов API с ошибками валидации.

Структура соответствует формату FastAPI / Pydantic v2:
тело 422 обычно выглядит как ``{"detail": [{...}, ...]}``,
а внутри каждого элемента используются ключи ``loc``, ``msg``, ``ctx``.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ValidationErrorSchema(BaseModel):
    """Одна ошибка валидации из массива ``detail``.

    Attributes:
        type: Тип ошибки (например, ``value_error``).
        location: Путь к полю с ошибкой (в JSON — ``loc``),
            например ``["body", "email"]``.
        message: Текст ошибки (в JSON — ``msg``).
        input: Значение, которое не прошло валидацию.
        context: Дополнительный контекст (в JSON — ``ctx``).
            Может отсутствовать в ответе API, поэтому поле опционально.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: str
    location: list[str] = Field(alias="loc")
    message: str = Field(alias="msg")
    input: Any
    context: dict[str, Any] | None = Field(default=None, alias="ctx")


class ValidationErrorResponseSchema(BaseModel):
    """Тело ответа API при ошибке валидации (обычно HTTP 422).

    Attributes:
        details: Список ошибок валидации (в JSON — ``detail``).
    """

    model_config = ConfigDict(populate_by_name=True)

    details: list[ValidationErrorSchema] = Field(alias="detail")
