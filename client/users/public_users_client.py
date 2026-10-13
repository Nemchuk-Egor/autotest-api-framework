"""Публичный клиент для работы с API пользователей (без авторизации)."""

import allure
from httpx import Response

from client.api_client import ApiClient
from client.public_http_builder import get_public_http_client
from client.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    CreateUserRequestNegativeSchema,
)
from tools.http.routes import ApiRoutes


class PublicUserClient(ApiClient):
    """Клиент для публичных операций с пользователями.

    Наследует методы ``get`` / ``post`` / ``patch`` / ``delete``
    от ``ApiClient`` и добавляет методы предметной области
    (создание пользователя и т.д.).
    """

    @allure.step("Создать пользователя")
    def create_user_api(
        self,
        request: CreateUserRequestSchema | CreateUserRequestNegativeSchema,
    ) -> Response:
        """Создаёт пользователя и возвращает «сырой» HTTP-ответ.

        Используйте этот метод, когда нужно проверить статус-код,
        заголовки или тело ответа «как есть».
        Принимает и позитивную, и негативную схему запроса.

        Args:
            request: Данные нового пользователя (валидные или намеренно
                невалидные — через ``CreateUserRequestNegativeSchema``).

        Returns:
            Ответ сервера (``httpx.Response``).
        """
        return self.post(ApiRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """Создаёт пользователя и возвращает уже разобранный ответ.

        После запроса тело ответа парсится в ``CreateUserResponseSchema``.
        Удобно, когда нужны типизированные поля (``user.id``, ``user.email`` и т.д.).

        Args:
            request: Данные нового пользователя (Pydantic-схема).

        Returns:
            Разобранный ответ API с данными созданного пользователя.
        """
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_user_client() -> PublicUserClient:
    """Фабрика: создаёт ``PublicUserClient`` с публичным HTTP-клиентом.

    Returns:
        Готовый к использованию ``PublicUserClient``.
    """
    return PublicUserClient(get_public_http_client())
