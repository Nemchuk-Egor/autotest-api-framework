"""Базовые assertion-функции для API-тестов.

Вместо «голых» ``assert`` в тестах используются эти обёртки:
при падении они показывают понятное сообщение с ожидаемым
и фактическим значением, а также с именем проверяемого поля.
"""

from typing import Any

import allure


@allure.step("Проверить, что статус-код равен {expected}")
def assert_status_code(actual: int, expected: int) -> None:
    """Проверяет, что HTTP-статус ответа совпадает с ожидаемым.

    Args:
        actual: Фактический статус-код из ответа (например, ``response.status_code``).
        expected: Ожидаемый статус-код (например, ``HTTPStatus.OK``).

    Raises:
        AssertionError: Если статус-коды не совпадают.
    """
    assert actual == expected, f"Expected status code {expected}, but got {actual}"


@allure.step("Проверить, что {name} равен {expected}")
def assert_equal(actual: Any, expected: Any, name: str) -> None:
    """Проверяет равенство двух значений с указанием имени поля.

    Args:
        actual: Фактическое значение из ответа API.
        expected: Ожидаемое значение (часто из тела запроса).
        name: Человекочитаемое имя поля для сообщения об ошибке
            (например, ``"email"`` или ``"first_name"``).

    Raises:
        AssertionError: Если значения не равны.
    """
    assert actual == expected, f"Expected {name} to be {expected}, but got {actual}"


@allure.step("Проверить, что {name} заполнен")
def assert_is_true(actual: Any, name: str) -> None:
    """Проверяет, что значение истинно (truthy) в смысле Python.

    Полезно для проверки, что объект/поле не пустое и не ``None``.

    Args:
        actual: Проверяемое значение.
        name: Имя поля для сообщения об ошибке.

    Raises:
        AssertionError: Если значение ложно (falsy): ``None``, ``False``, ``0``, ``""`` и т.п.
    """
    assert actual, f"Expected {name} to be True, but got {actual}"
