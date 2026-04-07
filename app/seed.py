from app.db import engine
from sqlalchemy import text
from argon2 import PasswordHasher
from datetime import datetime

ph = PasswordHasher()

def run_seed():
    with engine.connect() as conn:
        # ----------------- Роли -----------------
        roles = ["admin", "manager", "user"]
        role_ids = {}

        for role_name in roles:
            result = conn.execute(
                text("SELECT id FROM roles WHERE name = :name"),
                {"name": role_name}
            ).fetchone()
            if not result:
                conn.execute(
                    text("INSERT INTO roles (name) VALUES (:name)"),
                    {"name": role_name}
                )
                result = conn.execute(
                    text("SELECT id FROM roles WHERE name = :name"),
                    {"name": role_name}
                ).fetchone()
            role_ids[role_name] = result[0]

        # ----------------- Категории -----------------
        category_name = "users"
        category_result = conn.execute(
            text("SELECT id FROM categories WHERE name = :name"),
            {"name": category_name}
        ).fetchone()

        if not category_result:
            conn.execute(
                text("INSERT INTO categories (name) VALUES (:name)"),
                {"name": category_name}
            )
            category_result = conn.execute(
                text("SELECT id FROM categories WHERE name = :name"),
                {"name": category_name}
            ).fetchone()

        category_id = category_result[0]

        # ----------------- Пермишны -----------------
        perms = [
            # admin: всё
            {
                "role_id": role_ids["admin"],
                "category_id": category_id,
                "can_read": True,
                "can_create": True,
                "can_update": True,
                "can_delete": True
            },
            # manager: читать и обновлять
            {
                "role_id": role_ids["manager"],
                "category_id": category_id,
                "can_read": True,
                "can_create": False,
                "can_update": True,
                "can_delete": False
            },
            # user: только читать
            {
                "role_id": role_ids["user"],
                "category_id": category_id,
                "can_read": True,
                "can_create": False,
                "can_update": False,
                "can_delete": False
            }
        ]

        for perm in perms:
            exists = conn.execute(
                text(
                    "SELECT id FROM permissions WHERE role_id = :role_id AND category_id = :category_id"
                ),
                {"role_id": perm["role_id"], "category_id": perm["category_id"]}
            ).fetchone()
            if not exists:
                conn.execute(
                    text(
                        "INSERT INTO permissions (role_id, category_id, can_read, can_create, can_update, can_delete) "
                        "VALUES (:role_id, :category_id, :can_read, :can_create, :can_update, :can_delete)"
                    ),
                    perm
                )

        # ----------------- Юзеры -----------------
        users = [
            {"email": "admin@example.com", "password": "admin123", "role": "admin"},
            {"email": "manager@example.com", "password": "manager123", "role": "manager"},
            {"email": "user@example.com", "password": "user123", "role": "user"},
        ]

        for u in users:
            result = conn.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": u["email"]}
            ).fetchone()

            if not result:
                password_digest = ph.hash(u["password"])
                now = datetime.utcnow()
                conn.execute(
                    text(
                        "INSERT INTO users (email, password_digest, is_active, created_at) "
                        "VALUES (:email, :password_digest, :is_active, :created_at)"
                    ),
                    {
                        "email": u["email"],
                        "password_digest": password_digest,
                        "is_active": True,
                        "created_at": now
                    }
                )
                user_id = conn.execute(
                    text("SELECT id FROM users WHERE email = :email"),
                    {"email": u["email"]}
                ).fetchone()[0]
                # Привязка роли через user_roles
                conn.execute(
                    text(
                        "INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"
                    ),
                    {"user_id": user_id, "role_id": role_ids[u["role"]]}
                )
                print(f"Seed: user {u['email']} created")
            else:
                print(f"Seed: user {u['email']} already exists")

        conn.commit()
        print("Seed finished successfully!")


if __name__ == "__main__":
    run_seed()
