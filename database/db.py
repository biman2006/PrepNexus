import os
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_env(key):
    value = os.getenv(key)
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return value

DB_HOST = get_env("DB_HOST")
DB_USER = get_env("DB_USER")
DB_PASSWORD = get_env("DB_PASSWORD")
DB_NAME = get_env("DB_NAME")
SQLITE_DB_PATH = get_env("SQLITE_DB_PATH")

# Resolve SQLite path with Streamlit Cloud-friendly default when not on Windows.
if not SQLITE_DB_PATH:
    if os.name == "nt":
        SQLITE_DB_PATH = "prepnexus.db"
    else:
        SQLITE_DB_PATH = "/tmp/prepnexus.db"

sqlite_dir = os.path.dirname(SQLITE_DB_PATH)
if sqlite_dir and not os.path.exists(sqlite_dir):
    os.makedirs(sqlite_dir, exist_ok=True)

sqlite_url = f"sqlite:///{SQLITE_DB_PATH}"

# Prefer MySQL when credentials are provided; fall back to SQLite for local/testing.
if DB_HOST and DB_USER and DB_PASSWORD and DB_NAME:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        # attempt a quick connection to validate settings
        with engine.connect() as conn:
            pass
        logger.info("Connected to MySQL database at %s, using database %s", DB_HOST, DB_NAME)
    except Exception as e:
        logger.warning("Could not connect to MySQL at %s; falling back to SQLite %s: %s", DB_HOST, SQLITE_DB_PATH, e)
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        logger.info("Using SQLite database at %s", SQLITE_DB_PATH)
else:
    logger.info("MySQL credentials not fully provided; using SQLite database at %s.", SQLITE_DB_PATH)
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
