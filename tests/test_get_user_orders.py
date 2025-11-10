import requests
import allure
from data.urls import Urls


class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, create_user):
        response = requests.get(
            Urls.ORDERS,
            headers={"Authorization": create_user["token"]}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        assert "total" in response.json()
        assert isinstance(response.json()["total"], int)
        assert "totalToday" in response.json()
        assert isinstance(response.json()["totalToday"], int)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = requests.get(Urls.ORDERS)
        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised"
        }
