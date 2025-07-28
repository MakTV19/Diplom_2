import pytest
import requests
import uuid
import allure
from data.urls import Urls




class TestUpdateUser:
    @allure.title("Обновление данных пользователя с авторизацией")
    @pytest.mark.parametrize("field, new_value", [
        ("email", f"updated_{uuid.uuid4()}@yandex.ru"),
        ("name", "UpdatedUser")
    ])
    def test_update_user_with_auth(self, create_user, field, new_value):
        update_data = {field: new_value}
        
        response = requests.patch(
            Urls.USER,
            json=update_data,
            headers={"Authorization": create_user["token"]}
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"][field] == new_value
        # Проверяем, что другие поля не изменились
        if field == "email":
            assert response.json()["user"]["name"] == create_user["name"]
        else:
            assert response.json()["user"]["email"] == create_user["email"]

    @allure.title("Обновление данных пользователя без авторизации")
    @pytest.mark.parametrize("field, new_value", [
        ("email", f"updated_{uuid.uuid4()}@yandex.ru"),
        ("name", "UpdatedUser")
    ])
    def test_update_user_without_auth(self, field, new_value):
        response = requests.patch(
            Urls.USER,
            json={field: new_value}
        )
        
        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised"
        }

    @allure.title("Обновление данных пользователя с невалидным токеном")
    def test_update_user_invalid_token(self):
        response = requests.patch(
            Urls.USER,
            json={"name": "NewName"},
            headers={"Authorization": "invalid_token"}
        )
        
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "message" in response.json()