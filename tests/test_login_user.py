import pytest
import requests
import uuid
import allure
from data.urls import Urls




class TestLoginUser:
    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user(self, create_user):
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"]
        }
        
        response = requests.post(Urls.LOGIN, json=login_data)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert response.json()["user"]["email"] == create_user["email"]
        assert response.json()["user"]["name"] == create_user["name"]

    @allure.title("Логин с некорректными данными")
    @pytest.mark.parametrize("invalid_data", [
        {"email": "wrong@yandex.ru", "password": "password123"},
        {"email": f"test_{uuid.uuid4()}@yandex.ru", "password": "wrongpassword"}
    ])
    def test_login_invalid_credentials(self, invalid_data):
        response = requests.post(Urls.LOGIN, json=invalid_data)
        
        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect"
        }

    @allure.title("Логин с пустыми данными")
    @pytest.mark.parametrize("empty_field", ["email", "password"])
    def test_login_empty_fields(self, empty_field):
        login_data = {
            "email": "test@yandex.ru",
            "password": "password123"
        }
        login_data[empty_field] = ""
        
        response = requests.post(Urls.LOGIN, json=login_data)
        
        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect"
        }