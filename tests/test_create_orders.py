import requests
import allure
from data.urls import Urls


class TestCreateOrder:
    @allure.title("Create order with authorization and valid ingredients")
    def test_create_order_with_auth(self, create_user, valid_ingredients):
        response = requests.post(
            Urls.ORDERS,
            json={"ingredients": valid_ingredients},
            headers={"Authorization": create_user["token"]}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()
        assert response.json()["order"]["number"] is not None

    
    @allure.title("Create order without authorization")
    def test_create_order_without_auth(self, valid_ingredients):
        response = requests.post(
            Urls.ORDERS,
            json={"ingredients": valid_ingredients}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "name" in response.json()
        assert "order" in response.json()
        assert response.json()["order"]["number"] is not None

    
    @allure.title("Create order without ingredients")
    def test_create_order_no_ingredients(self, create_user):
        response = requests.post(
            Urls.ORDERS,
            json={"ingredients": []},
            headers={"Authorization": create_user["token"]}
        )
        assert response.status_code == 400
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided"
        }

    
    @allure.title("Create order with invalid ingredient hash")
    def test_create_order_invalid_ingredient(self, create_user):
        response = requests.post(
            Urls.ORDERS,
            json={"ingredients": ["invalid_hash"]},
            headers={"Authorization": create_user["token"]}
        )
        assert response.status_code == 500
        assert response.json()["success"] is False
