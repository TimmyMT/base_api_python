# app/policies/user_policy.py
from app.models.user import User

class UserPolicy:
    def __init__(self, user: User):
        self.user = user

    def index(self) -> bool:
        # Только админ может смотреть список всех пользователей
        return self.user.role == "admin"

    def show(self, target_user: User) -> bool:
        # Админ видит всех, обычный пользователь видит только себя
        return self.user.role == "admin" or self.user.id == target_user.id

    def create(self) -> bool:
        # Только админ может создавать пользователей
        return self.user.role == "admin"

    def update(self, target_user: User) -> bool:
        # Админ может обновлять всех, пользователь только себя
        return self.user.role == "admin" or self.user.id == target_user.id

    def destroy(self, target_user: User) -> bool:
        # Только админ может удалять пользователей
        return self.user.role == "admin"
