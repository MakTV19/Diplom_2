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
    if response.status_code != 200:
        pytest.skip("Failed to create test user")
    
    token = response.json().get("accessToken")
    if not token:
        pytest.skip("No access token received")
    
    user_info = {"token": token, **user_data}
    
    yield user_info
    
    try:
        cleanup_response = requests.delete(
            Urls.USER, 
            headers={"Authorization": token},
            timeout=5
        )
        if cleanup_response.status_code != 200:
            print(f"Warning: Failed to delete test user. Status code: {cleanup_response.status_code}")
            print(f"Response: {cleanup_response.text}")
    except Exception as e:
        print(f"Warning: Exception during user deletion: {str(e)}")

@pytest.fixture
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов"""
    response = requests.get(Urls.INGREDIENTS)
    if response.status_code != 200:
        pytest.skip("Could not fetch ingredients")
    
    ingredients = response.json().get("data", [])
    if len(ingredients) < 2:
        pytest.skip("Not enough ingredients available")
    
    return [ingredients[0]["_id"], ingredients[1]["_id"]]