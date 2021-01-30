import os

# Hosts
RQ_DASHBOARD_REDIS_HOST = "redis"

# Secrets and keys
SECRET_KEY = "2b2eaed61f28ea8ac252ace5e862bea1eb258c03f5669b3a"
BUGSNAG_API_KEY = os.getenv("BUGSNAG_API_KEY")

# Cookies
SESSION_COOKIE_SAMESITE = "Lax"
