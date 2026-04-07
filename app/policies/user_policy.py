from fastapi import HTTPException
from app.models.user import User

class UserPolicy:
    def __init__(self, user: User):
        self.user = user

    # приватный метод для проверки
    def _authorize(self, condition: bool):
        if not condition:
            raise HTTPException(status_code=403, detail="Not authorized")
        return True

    # проверка, есть ли роль у пользователя
    def has_role(self, role_name: str) -> bool:
        return self.user.has_role(role_name)

    # доступ к списку пользователей
    def index(self):
        return self._authorize(
            self.has_role("admin") or self.has_role("manager")
        )

    # просмотр конкретного пользователя
    def show(self, target_user: User):
        return self._authorize(
            self.has_role("admin") or self.has_role("manager") or self.user.id == target_user.id
        )

    # создание пользователя
    def create(self):
        return self._authorize(self.has_role("admin"))

    # обновление пользователя
    def update(self, target_user: User):
        return self._authorize(
            self.has_role("admin") or self.has_role("manager") or self.user.id == target_user.id
        )

    # удаление пользователя
    def destroy(self, target_user: User):
        return self._authorize(self.has_role("admin"))
