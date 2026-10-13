"""Assertion-функции для проверок, связанных с пользователями.

Сравнивают поля ответа API с ожидаемыми значениями
(часто — с данными из тела запроса на создание пользователя).
"""

from typing import Any

import allure

from client.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertion.base import assert_equal, assert_is_true


@allure.step("Проверить поля пользователя")
def assert_user(actual: Any, expected: Any) -> None:
    """Сравнивает два объекта пользователя поле за полем.

    Проверяются: ``id``, ``email``, ``first_name``, ``last_name``, ``middle_name``.

    Args:
        actual: Фактический объект пользователя из ответа API.
        expected: Ожидаемый объект пользователя (эталон для сравнения).

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


@allure.step("Проверить ответ на создание пользователя")
def assert_create_user(
    actual: CreateUserResponseSchema, expected: CreateUserRequestSchema
) -> None:
    """Проверяет ответ на создание пользователя относительно тела запроса.

    Убеждается, что в ответе есть объект ``user``, а его персональные
    поля (email и ФИО) совпадают с данными из запроса.
    Поле ``id`` в запросе отсутствует (его выдаёт сервер), поэтому
    здесь оно не сравнивается.

    Args:
        actual: Разобранный ответ API (``CreateUserResponseSchema``).
        expected: Тело исходного запроса (``CreateUserRequestSchema``).

    Raises:
        AssertionError: Если ``user`` отсутствует или поля не совпадают.
    """
    assert_is_true(actual.user.id, "id")
    assert_equal(actual.user.email, expected.email, "email")
    assert_equal(actual.user.first_name, expected.first_name, "first_name")
    assert_equal(actual.user.last_name, expected.last_name, "last_name")
    assert_equal(actual.user.middle_name, expected.middle_name, "middle_name")
