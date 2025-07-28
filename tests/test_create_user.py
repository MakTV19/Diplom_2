import pytest
import requests
import allure
from data.urls import Urls





class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_data):
        response = requests.post(Urls.REGISTER, json=user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert response.json()["user"]["email"] == user_data["email"]
        assert response.json()["user"]["name"] == user_data["name"]

        # Удаляем созданного пользователя
        token = response.json().get("accessToken")
        requests.delete(Urls.USER, headers={"Authorization": token})

    @allure.title("Создание уже существующего пользователя")
    def test_create_existing_user(self, create_user, user_data):
        response = requests.post(Urls.REGISTER, json=user_data)
        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "User already exists"
        }

    @allure.title("Создание пользователя с отсутствующим обязательным полем")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, user_data, missing_field):
        data = user_data.copy()
        data[missing_field] = ""
        response = requests.post(Urls.REGISTER, json=data)
        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }