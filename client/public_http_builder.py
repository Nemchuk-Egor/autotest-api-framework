"""Фабрика публичного (без авторизации) HTTP-клиента."""

from httpx import Client

from config import settings


def get_public_http_client() -> Client:
    """Создаёт ``httpx.Client`` для публичных запросов к API.

    Клиент берёт ``base_url`` и ``timeout`` из настроек проекта
    (файл ``.env`` / переменные окружения). Авторизационные
    заголовки сюда не добавляются — это «гостевой» клиент.

    Returns:
        Настроенный экземпляр ``httpx.Client``.
    """
    return Client(
        timeout=settings.http_client.timeout,
        base_url=settings.http_client.client_url,
    )
