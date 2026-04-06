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

    def index(self):
        return self._authorize(self.user.role == "admin" or self.user.role == "manager")

    def show(self, target_user: User):
        return self._authorize(self.user.role == "admin" or self.user.role == "manager" or self.user.id == target_user.id)

    def create(self):
        return self._authorize(self.user.role == "admin")
    
    def change_role(self, target_user: User):
        return self._authorize(self.user.role == "admin" and target_user.role != "admin")

    def update(self, target_user: User):
        return self._authorize(self.user.role == "admin" or self.user.role == "manager" or self.user.id == target_user.id)

    def destroy(self, target_user: User):
        return self._authorize(self.user.role == "admin")
