"""Генератор фейковых (тестовых) данных на основе библиотеки Faker.

Используется в схемах запросов как ``default_factory``, чтобы
каждый новый объект получал уникальные email, ФИО и пароль.
"""

from faker import Faker


class Fake:
    """Обёртка над ``Faker`` с удобными методами для тестов.

    Args:
        faker: Экземпляр библиотеки Faker (с нужной локалью).
    """

    def __init__(self, faker: Faker):
        self.faker = faker

    def email(self, domain: str | None = None) -> str:
        """Генерирует случайный email.

        Args:
            domain: Домен email (например, ``"example.com"``).
                Если не указан — выбирается случайный.

        Returns:
            Строка с email-адресом.
        """
        return self.faker.email(domain=domain)

    def last_name(self) -> str:
        """Генерирует случайную фамилию."""
        return self.faker.last_name()

    def first_name(self) -> str:
        """Генерирует случайное имя."""
        return self.faker.first_name()

    def middle_name(self) -> str:
        """Генерирует случайное отчество."""
        return self.faker.middle_name()

    def uuid(self) -> str:
        """Генерирует случайный UUID в виде строки."""
        return self.faker.uuid4()

    def password(self) -> str:
        """Генерирует случайный пароль."""
        return self.faker.password()


# Единый генератор для всего проекта (русская локаль).
fake = Fake(Faker("ru_RU"))
