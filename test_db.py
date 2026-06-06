# test_connection.py

from database.db import engine

print(engine.url)

with engine.connect() as conn:
    print("CONNECTED SUCCESSFULLY")