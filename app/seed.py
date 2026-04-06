from app.db import SessionLocal
from app.models.user import User
from sqlalchemy import text
from argon2 import PasswordHasher

def run_seed():
    db = SessionLocal()
    ph = PasswordHasher()

    # Хэшируем пароль через argon2
    password_plain = "admin123"
    password_digest = ph.hash(password_plain)

    sql = text("""
    INSERT INTO users (email, password_digest, role)
    SELECT :email, :password_digest, :role
    WHERE NOT EXISTS (
        SELECT 1 FROM users WHERE email = :email
    )
    """)

    db.execute(sql, {
        "email": "admin@example.com",
        "password_digest": password_digest,
        "role": "admin"
    })

    db.commit()
    print("Seed: admin user created if not exists")
    db.close()

if __name__ == "__main__":
    run_seed()
