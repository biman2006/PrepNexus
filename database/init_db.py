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

    print("PrepNexus database initialized successfully.")




if __name__=="__main__":
    initialize_database()