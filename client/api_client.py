"""Базовый HTTP-клиент для работы с API.

Обёртка над библиотекой ``httpx``, чтобы в тестах и клиентах
вызывать методы ``get``, ``post``, ``patch``, ``delete`` единообразно.
"""

from typing import Any

import allure

from httpx import Client, URL, Response
from httpx._types import QueryParamTypes, RequestData, RequestFiles


class ApiClient:
    """Базовый клиент для отправки HTTP-запросов к API.

    Принимает уже настроенный экземпляр ``httpx.Client``
    (с ``base_url``, ``timeout`` и т.д.) и делегирует ему запросы.
    """

    def __init__(self, client: Client):
        """Сохраняет HTTP-клиент для дальнейших запросов.

        Args:
            client: Настроенный экземпляр ``httpx.Client``.
        """
        self.client = client

    @allure.step("Отправить GET-запрос на {url}")
    def get(self, url: URL | str, params: QueryParamTypes) -> Response:
        """Отправляет GET-запрос.

        Args:
            url: Путь или полный URL эндпоинта.
            params: Query-параметры запроса (словарь или другие типы httpx).

        Returns:
            Ответ сервера (``httpx.Response``).
        """
        return self.client.get(url, params=params)

    @allure.step("Отправить POST-запрос на {url}")
    def post(
        self,
        url: URL | str,
        json: Any | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
    ) -> Response:
        """Отправляет POST-запрос.

        Args:
            url: Путь или полный URL эндпоинта.
            json: Тело запроса в формате JSON (будет сериализовано httpx).
            data: Тело запроса в формате form-data.
            files: Файлы для загрузки (multipart).

        Returns:
            Ответ сервера (``httpx.Response``).
        """
        return self.client.post(url, json=json, data=data, files=files)

    @allure.step("Отправить PATCH-запрос на {url}")
    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """Отправляет PATCH-запрос (частичное обновление ресурса).

        Args:
            url: Путь или полный URL эндпоинта.
            json: Тело запроса в формате JSON.

        Returns:
            Ответ сервера (``httpx.Response``).
        """
        return self.client.patch(url, json=json)

    @allure.step("Отправить DELETE-запрос на {url}")
    def delete(self, url: URL | str) -> Response:
        """Отправляет DELETE-запрос.

        Args:
            url: Путь или полный URL эндпоинта.

        Returns:
            Ответ сервера (``httpx.Response``).
        """
        return self.client.delete(url)
