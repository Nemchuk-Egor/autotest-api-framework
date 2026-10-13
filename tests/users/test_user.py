"""Тесты API пользователей (создание и связанные сценарии)."""

from http import HTTPStatus

import allure
import pytest

from client.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema
from client.users.public_users_client import PublicUserClient
from client.users.users_schema import (
    CreateUserRequestNegativeSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from tools.allure.epic import AllureEpic
from tools.allure.feature import AllureFeature
from tools.allure.story import AllureStory
from tools.assertion.base import assert_status_code
from tools.assertion.errors import assert_validation_response_error
from tools.assertion.users import assert_create_user
from tools.assertion.validation import validate_json_schema


@pytest.mark.regression
@pytest.mark.users
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
class TestUser:
    """Набор тестов для операций с пользователями."""

    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Успешное создание пользователя")
    def test_create_user(self, public_user_client: PublicUserClient):
        """Проверяет успешное создание пользователя.

        Шаги:
            1. Формирует тело запроса со случайными данными (через ``fake``).
            2. Вызывает публичный эндпоинт создания пользователя.
            3. Проверяет HTTP-статус ``200 OK``.
            4. Сравнивает email и ФИО в ответе с данными из запроса.
            5. Валидирует тело ответа по JSON Schema Pydantic-модели.
        """
        request = CreateUserRequestSchema()
        response = public_user_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Негативное создание пользователя с невалидным email")
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "email, expected_error",
        [
            pytest.param(
                "",
                ValidationErrorSchema(
                    type="value_error",
                    location=["body", "email"],
                    message=(
                        "value is not a valid email address: "
                        "An email address must have an @-sign."
                    ),
                    input="",
                    context={"reason": "An email address must have an @-sign."},
                ),
                id="empty_email",
            ),
        ],
    )
    def test_create_user_with_negative_email(
        self,
        public_user_client: PublicUserClient,
        email: str,
        expected_error: ValidationErrorSchema,
    ):
        """Проверяет, что API отклоняет создание пользователя с невалидным email.

        Параметры (``email``, ``expected_error``) задаются через ``parametrize``:
        каждый кейс — отдельный прогон теста с своим id в отчёте.

        Шаги:
            1. Собирает ожидаемый ответ 422 из эталонной ошибки.
            2. Отправляет запрос с намеренно невалидным email.
            3. Проверяет HTTP-статус ``422 Unprocessable Entity``.
            4. Сравнивает тело ошибки с эталоном.
            5. Валидирует тело ответа по JSON Schema.
        """
        expected_response_error = ValidationErrorResponseSchema(detail=[expected_error])
        request = CreateUserRequestNegativeSchema(email=email)
        response = public_user_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # UNPROCESSABLE_ENTITY = 422; имя UNPROCESSABLE_CONTENT есть только в Python 3.13+.
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_response_error(response_data, expected_response_error)

        validate_json_schema(response.json(), response_data.model_json_schema())
