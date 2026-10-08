"""Session management utilities."""

import base64
import random
import string
from datetime import datetime, timedelta


class SessionManager:
    SESSION_DURATION_HOURS = 12

    @staticmethod
    def generate_session_key() -> str:
        random_part = "".join(random.choices(string.ascii_letters + string.digits, k=28))
        expiry_time = datetime.utcnow() + timedelta(hours=SessionManager.SESSION_DURATION_HOURS)
        expiry_str = expiry_time.strftime("%Y%m%d%H%M%S")
        encoded_expiry = base64.b64encode(expiry_str.encode()).decode()
        return f"{random_part}.{encoded_expiry}"

    @staticmethod
    def validate_session_key(session_key: str) -> bool:
        try:
            parts = session_key.split(".")
            if len(parts) != 2:
                return False
            expiry_str = base64.b64decode(parts[1]).decode()
            expiry_time = datetime.strptime(expiry_str, "%Y%m%d%H%M%S")
            return datetime.utcnow() < expiry_time
        except Exception:
            return False
