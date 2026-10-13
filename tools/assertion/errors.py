"""Assertion-функции для проверки ответов API с ошибками валидации."""

import allure

from client.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema
from tools.assertion.base import assert_equal, assert_length


@allure.step("Проверить одну ошибку валидации")
def assert_validation_error(
    actual: ValidationErrorSchema, expected: ValidationErrorSchema
) -> None:
    """Сравнивает одну ошибку валидации поле за полем.

    Args:
        actual: Фактическая ошибка из ответа API.
        expected: Ожидаемая ошибка (эталон из теста).

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.location, expected.location, "location")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")


@allure.step("Проверить ответ с ошибками валидации")
def assert_validation_response_error(
    actual: ValidationErrorResponseSchema, expected: ValidationErrorResponseSchema
) -> None:
    """Сравнивает полный ответ 422: число ошибок и каждую ошибку по очереди.

    Args:
        actual: Фактический ответ API (``ValidationErrorResponseSchema``).
        expected: Ожидаемый ответ с эталонным списком ``details``.

    Raises:
        AssertionError: Если длина списка или содержимое ошибок не совпадает.
    """
    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)
