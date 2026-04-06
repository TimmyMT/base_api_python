from app.db import engine
from sqlalchemy import text
from argon2 import PasswordHasher
from datetime import datetime

ph = PasswordHasher()

def run_seed():
    with engine.connect() as conn:
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
                        "INSERT INTO users (email, password_digest, role, is_active, created_at) "
                        "VALUES (:email, :password_digest, :role, :is_active, :created_at)"
                    ),
                    {
                        "email": u["email"],
                        "password_digest": password_digest,
                        "role": u["role"],
                        "is_active": True,
                        "created_at": now
                    }
                )
                print(f"Seed: user {u['email']} created")
            else:
                print(f"Seed: user {u['email']} already exists")

        conn.commit()
