class BasePolicy:
    def __init__(self, user: User):
        self.user = user

    def _authorize(self, condition: bool):
        if not condition:
            raise HTTPException(status_code=403, detail="Not authorized")
        return True

    def _has_permission(self, category_name: str, action: str) -> bool:
        """
        Проверка прав пользователя на категорию по имени.
        action: "read", "create", "update", "delete"
        """
        field_name = f"can_{action}"  # например "can_read", "can_create"
        for role in self.user.roles:
            for perm in role.permissions:
                if perm.category.name == category_name and getattr(perm, field_name, False):
                    return True
        return False

    # CRUD методы
    def can_read(self, category_name: str):
        return self._authorize(self._has_permission(category_name, "read"))

    def can_create(self, category_name: str):
        return self._authorize(self._has_permission(category_name, "create"))

    def can_update(self, category_name: str):
        return self._authorize(self._has_permission(category_name, "update"))

    def can_delete(self, category_name: str):
        return self._authorize(self._has_permission(category_name, "delete"))

    def can_own(self, resource_owner_id: int):
        return self._authorize(self.user.id == resource_owner_id)
