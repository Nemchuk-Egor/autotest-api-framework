"""Pydantic-схемы запросов и ответов API пользователей.

Схемы описывают структуру JSON: какие поля есть, какого они типа
и как называются в API (через ``alias``, если имя в Python и в JSON отличается).
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from tools.faker import fake


class UserSchema(BaseModel):
    """Данные пользователя, которые возвращает API.

    Attributes:
        id: Уникальный идентификатор пользователя.
        email: Email пользователя.
        last_name: Фамилия.
        first_name: Имя.
        middle_name: Отчество.
    """

    model_config = ConfigDict(populate_by_name=True)
    id: str
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str


class CreateUserRequestSchema(BaseModel):
    """Тело запроса на создание пользователя.

    По умолчанию поля заполняются случайными данными через ``fake``,
    чтобы в тестах не писать одни и те же значения вручную.
    Для полей с ``alias`` при сериализации в JSON используются
    имена API (например, ``lastName`` вместо ``last_name``).

    Attributes:
        email: Email нового пользователя.
        password: Пароль.
        last_name: Фамилия (в JSON — ``lastName``).
        first_name: Имя (в JSON — ``firstName``).
        middle_name: Отчество (в JSON — ``middleName``).
    """

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)


class CreateUserResponseSchema(BaseModel):
    """Тело ответа API после успешного создания пользователя.

    Attributes:
        user: Объект созданного пользователя.
    """

    user: UserSchema
