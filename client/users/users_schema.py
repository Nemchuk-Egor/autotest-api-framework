"""Pydantic-схемы запросов и ответов API пользователей.

Схемы описывают структуру JSON: какие поля есть, какого они типа
и как называются в API (через ``alias``, если имя в Python и в JSON отличается).
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from tools.faker import fake


class UserSchema(BaseModel):
    """Данные пользователя, которые возвращает API.

    Для ФИО в JSON используются camelCase-имена (``lastName`` и т.д.),
    а в Python-коде — snake_case. Это возможно благодаря ``alias``
    и ``populate_by_name=True``.

    Attributes:
        id: Уникальный идентификатор пользователя.
        email: Email пользователя.
        last_name: Фамилия (в JSON — ``lastName``).
        first_name: Имя (в JSON — ``firstName``).
        middle_name: Отчество (в JSON — ``middleName``).
    """

    model_config = ConfigDict(populate_by_name=True)
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


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

    model_config = ConfigDict(populate_by_name=True)
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


class CreateUserRequestNegativeSchema(BaseModel):
    """Тело запроса для **негативных** сценариев создания пользователя.

    В отличие от ``CreateUserRequestSchema``, здесь типы полей широкие
    (``str | int | None``), чтобы тест мог осознанно отправить
    невалидные значения (пустой email, ``None``, число и т.д.).
    Позитивная схема с ``EmailStr`` такое тело просто не собрала бы.

    Attributes:
        email: Email (допускаются невалидные значения).
        password: Пароль (допускаются невалидные значения).
        last_name: Фамилия (в JSON — ``lastName``).
        first_name: Имя (в JSON — ``firstName``).
        middle_name: Отчество (в JSON — ``middleName``).
    """

    model_config = ConfigDict(populate_by_name=True)
    email: str | int | None = Field(default_factory=fake.email)
    password: str | int | None = Field(default_factory=fake.password)
    last_name: str | int | None = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str | int | None = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str | int | None = Field(alias="middleName", default_factory=fake.middle_name)
