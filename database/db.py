import os
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

logging.basicConfig()
logger = logging.getLogger(__name__)

# Prefer MySQL when credentials are provided; fall back to SQLite for local testing
if DB_HOST and DB_USER and DB_PASSWORD and DB_NAME:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        # attempt a quick connection to validate settings
        with engine.connect() as conn:
            pass
    except Exception as e:
        logger.warning("Could not connect to MySQL at %s, falling back to SQLite: %s", DB_HOST, e)
        engine = create_engine("sqlite:///prepnexus.db")
else:
    logger.info("MySQL credentials not fully provided; using SQLite for local development.")
    engine = create_engine("sqlite:///prepnexus.db")
