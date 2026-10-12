"""Pytest-фикстуры, связанные с пользователями."""

import pytest

from client.users.public_users_client import PublicUserClient, get_public_user_client


@pytest.fixture
def public_user_client() -> PublicUserClient:
    """Фикстура: публичный клиент API пользователей.

    Передаётся в тест как аргумент с тем же именем::

        def test_create_user(public_user_client: PublicUserClient):
            ...

    Returns:
        Экземпляр ``PublicUserClient`` без авторизации.
    """
    return get_public_user_client()
