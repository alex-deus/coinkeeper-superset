import os

SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY")

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://redis:6379/0",
}

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

ROW_LIMIT = 0
