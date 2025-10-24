class Urls:
    BASE = "https://stellarburgers.nomoreparties.site/api"
    
    # Auth endpoints
    REGISTER = f"{BASE}/auth/register"
    LOGIN = f"{BASE}/auth/login"
    USER = f"{BASE}/auth/user"
    
    # Ingredients endpoints
    INGREDIENTS = f"{BASE}/ingredients"
    
    # Orders endpoints
    ORDERS = f"{BASE}/orders"