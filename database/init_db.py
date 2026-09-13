import os

from sqlalchemy import inspect, text
from .db import engine
from .models import Base


def initialize_database():

    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "users" in inspector.get_table_names():
        columns = [column["name"] for column in inspector.get_columns("users")]
        if "password_hash" not in columns:
            try:
                with engine.connect() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
                    print("Added password_hash column to users table.")
            except Exception as exc:
                print(f"Could not migrate users table schema: {exc}")

        migrations = {
            "role": "VARCHAR(32) NOT NULL DEFAULT 'user'",
            "is_active": "INTEGER NOT NULL DEFAULT 1",
        }
        for column_name, column_definition in migrations.items():
            if column_name not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text(
                            f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}"
                        ))
                except Exception as exc:
                    print(f"Could not add users.{column_name}: {exc}")

        admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
        if admin_email:
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE users SET role = 'admin' WHERE lower(email) = :email"),
                    {"email": admin_email},
                )

    print("PrepNexus database initialized successfully.")




if __name__=="__main__":
    initialize_database()