"""Тесты API пользователей (создание и связанные сценарии)."""

from http import HTTPStatus

import pytest

from client.users.public_users_client import PublicUserClient
from client.users.users_schema import CreateUserRequestSchema


@pytest.mark.regression
@pytest.mark.users
class TestUser:
    """Набор тестов для операций с пользователями."""

    def test_create_user(self, public_user_client: PublicUserClient):
        """Проверяет успешное создание пользователя (статус 200 OK).

        Шаги:
            1. Формирует тело запроса со случайными данными.
            2. Вызывает публичный эндпоинт создания пользователя.
            3. Ожидает HTTP-статус ``200 OK``.
        """
        request = CreateUserRequestSchema()
        response = public_user_client.create_user_api(request)

        assert response.status_code == HTTPStatus.OK
