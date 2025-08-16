from os import getenv

POSTGRES_USER = getenv("POSTGRES_USER", "nhandt")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "DT123456")
POSTGRES_DB = getenv("POSTGRES_DB", "trading_analytics")
POSTGRES_HOST = getenv("POSTGRES_HOST", "trading-analytics-db")
POSTGRES_PORT = getenv("POSTGRES_PORT", 5432)
