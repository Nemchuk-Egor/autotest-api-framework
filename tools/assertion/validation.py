"""Валидация тела ответа API по JSON Schema.

Используется библиотека ``jsonschema`` с диалектом Draft 2020-12.
Схему удобно брать из Pydantic-модели через ``model_json_schema()``.
"""

from typing import Any

from jsonschema import Draft202012Validator, validate


def validate_json_schema(instance: Any, schema: dict) -> None:
    """Проверяет, что JSON-данные соответствуют заданной JSON Schema.

    Args:
        instance: Данные для проверки (обычно ``response.json()``).
        schema: Словарь JSON Schema (например, результат
            ``CreateUserResponseSchema.model_json_schema()``).

    Raises:
        jsonschema.exceptions.ValidationError: Если данные не соответствуют схеме.
    """
    validate(instance, schema, Draft202012Validator)
