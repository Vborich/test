from environs import Env

env = Env()
env.read_env()

DATABASE_CONFIG = {
    "connections": {"default": "postgres://" + env("POSTGRES_USER")
        + ":" + env("POSTGRES_PASSWORD") + "@" + env("POSTGRES_HOST") + ":5432/" + env("POSTGRES_DB")},
    "apps": {
        "models": {
            "models": ["src.models.Cart", "src.models.Product", "src.models.User", "aerich.models"],
            "default_connection": "default",
        },
    },
}

DATABASE_TEST_CONFIG = {
    "connections": {"default": env("DATABASE_TEST_CONNECTION")},
    "apps": {
        "models": {
            "models": ["src.models.Cart", "src.models.Product", "src.models.User", "aerich.models"],
            "default_connection": "default",
        }
    },
}

SECRET_KEY = env("SECRET_KEY")
ALGORITHM = env("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env("ACCESS_TOKEN_EXPIRE_MINUTES")
