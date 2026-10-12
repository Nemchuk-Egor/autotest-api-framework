"""Корневой conftest pytest.

Подключает pytest-плагины (фикстуры) из пакета ``fixtures``,
чтобы они были доступны во всех тестах проекта.
"""

pytest_plugins = (
    "fixtures.user",
)
