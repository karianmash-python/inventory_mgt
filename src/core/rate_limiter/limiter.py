from slowapi import Limiter
from src.core.rate_limiter.key_functions import user_or_ip_key_func

# Rate limiter with per-user (or IP fallback) logic
limiter = Limiter(
    key_func=user_or_ip_key_func,
    default_limits=["200/minute"]
)
