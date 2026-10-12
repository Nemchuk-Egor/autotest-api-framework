"""Конфигурация проекта на основе переменных окружения.

Настройки читаются из файла ``.env`` (и/или из переменных окружения)
через ``pydantic-settings``. Пример переменных:

* ``HTTP_CLIENT.URL`` — базовый URL API
* ``HTTP_CLIENT.TIMEOUT`` — таймаут HTTP-запросов в секундах
"""

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HttpClientConfig(BaseModel):
    """Настройки HTTP-клиента.

    Attributes:
        url: Базовый URL API (например, ``http://localhost:8000``).
        timeout: Максимальное время ожидания ответа в секундах.
    """

    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        """Возвращает базовый URL в виде строки для ``httpx.Client``.

        ``HttpUrl`` — специальный тип Pydantic; ``httpx`` ожидает ``str``,
        поэтому здесь выполняется явное преобразование.
        """
        return str(self.url)


class Settings(BaseSettings):
    """Корневые настройки приложения / тестового фреймворка.

    ``env_nested_delimiter="."`` позволяет задавать вложенные поля
    через точку в имени переменной, например ``HTTP_CLIENT.URL``.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="."
    )

    http_client: HttpClientConfig


# Единый экземпляр настроек на весь проект.
# Импортируйте его так: ``from config import settings``.
settings = Settings()
