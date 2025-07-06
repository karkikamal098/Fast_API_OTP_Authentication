from datetime import datetime, timedelta

otp_data = {}

def save_otp(email: str, otp: str, ttl_minutes: int = 5):
    otp_data[email] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=ttl_minutes)
    }

def verify_otp(email: str, submitted_otp: str) -> bool:
    record = otp_data.get(email)
    if not record:
        return False
    if record["expires_at"] < datetime.utcnow():
        otp_data.pop(email, None)
        return False
    if record["otp"] != submitted_otp:
        return False
    otp_data.pop(email, None)
    return True