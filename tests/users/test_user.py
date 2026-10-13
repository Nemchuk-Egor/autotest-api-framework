"""Тесты API пользователей (создание и связанные сценарии)."""

from http import HTTPStatus

import pytest

from client.users.public_users_client import PublicUserClient
from client.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertion.validation import validate_json_schema
from tools.assertion.base import assert_status_code
from tools.assertion.users import assert_create_user


@pytest.mark.regression
@pytest.mark.users
class TestUser:
    """Набор тестов для операций с пользователями."""

    def test_create_user(self, public_user_client: PublicUserClient):
        """Проверяет успешное создание пользователя.

        Шаги:
            1. Формирует тело запроса со случайными данными (через ``fake``).
            2. Вызывает публичный эндпоинт создания пользователя.
            3. Проверяет HTTP-статус ``200 OK``.
            4. Сравнивает email и ФИО в ответе с данными из запроса.
            5. Валидирует тело ответа по JSON Schema Pydantic-модели.
        """
        request = CreateUserRequestSchema()
        response = public_user_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())
