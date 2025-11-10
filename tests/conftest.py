import pytest
import requests
import uuid
from data.urls import Urls

@pytest.fixture
def user_data():
    """Фикстура для создания тестовых данных пользователя"""
    email = f"test_{uuid.uuid4()}@yandex.ru"
    password = "password123"
    name = "TestUser"
    return {"email": email, "password": password, "name": name}

@pytest.fixture
def create_user(user_data):
    """Фикстура для создания и удаления тестового пользователя"""
    response = requests.post(Urls.REGISTER, json=user_data)
    
    token = response.json().get("accessToken")
    
    user_info = {"token": token, **user_data}
    
    yield user_info
    
    requests.delete(
        Urls.USER, 
        headers={"Authorization": token}
    )

@pytest.fixture
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов"""
    response = requests.get(Urls.INGREDIENTS)
    
    ingredients = response.json().get("data", [])
    
    return [ingredients[0]["_id"], ingredients[1]["_id"]]
