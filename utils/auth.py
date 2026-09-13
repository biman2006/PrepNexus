import os
import re
import secrets
import smtplib
import socket
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from dotenv import load_dotenv

# =====================================================
# BASE DIRECTORY & LOAD .ENV
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path, override=True)

# =====================================================
# JWT CONFIGURATION
# =====================================================
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "prepnexus_super_secret_jwt_key_2026_prod")
JWT_ALGORITHM = "HS256"
JWT_ISSUER = "PrepNexus"


def create_jwt_token(user_id: int, email: str, name: str = "", role: str = "user", expires_in_hours: int = 24) -> str:
    """
    Generate a signed JWT token containing user identity and authorization claims.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "email": email.strip().lower(),
        "name": name,
        "role": role,
        "iss": JWT_ISSUER,
        "iat": now,
        "exp": now + timedelta(hours=expires_in_hours)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    """
    Decode and validate a JWT token string.
    Returns payload dictionary if valid, or None if expired/invalid.
    """
    if not token or not isinstance(token, str):
        return None
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_iss": True},
            issuer=JWT_ISSUER
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as exc:
        print(f"JWT decode error: {exc}")
        return None


def verify_jwt_session(token: str) -> dict:
    """
    Validates JWT token payload and checks user status against database.
    Returns user dict if session is valid and active, else None.
    """
    payload = decode_jwt_token(token)
    if not payload or "user_id" not in payload:
        return None

    from database.crud import get_user_by_id
    user = get_user_by_id(payload["user_id"])
    if not user or not user.is_active:
        return None

    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name or "",
        "role": user.role,
        "exp": payload.get("exp"),
        "token": token
    }


def get_jwt_token_claims(token: str) -> dict:
    """
    Extract readable claims and human-friendly expiration from a JWT token.
    """
    payload = decode_jwt_token(token)
    if not payload:
        return {}
    
    exp_timestamp = payload.get("exp")
    expires_str = "Unknown"
    time_remaining_str = ""
    if exp_timestamp:
        try:
            exp_dt = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            expires_str = exp_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            now_dt = datetime.now(timezone.utc)
            delta = exp_dt - now_dt
            if delta.total_seconds() > 0:
                hours = int(delta.total_seconds() // 3600)
                minutes = int((delta.total_seconds() % 3600) // 60)
                time_remaining_str = f"{hours}h {minutes}m remaining"
            else:
                time_remaining_str = "Expired"
        except Exception:
            pass

    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("email"),
        "name": payload.get("name"),
        "role": payload.get("role"),
        "issuer": payload.get("iss"),
        "expires_at": expires_str,
        "time_remaining": time_remaining_str
    }

# =====================================================
# FETCH EMAIL CREDENTIALS
# =====================================================

EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)


# =====================================================
# GENERATE OTP
# =====================================================

def generate_otp():
    """
    Generates a secure 6-digit OTP.
    """

    return str(secrets.randbelow(900000) + 100000)


# =====================================================
# PASSWORD HASHING
# =====================================================

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    )
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    if not isinstance(password, str) or not isinstance(stored_hash, str):
        return False

    try:
        salt, hash_hex = stored_hash.split("$", 1)
        if not salt or len(hash_hex) != 64:
            return False
        test_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            200000
        ).hex()
    except (TypeError, ValueError, UnicodeError):
        return False

    return secrets.compare_digest(test_hash, hash_hex)


def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    return bool(
        re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
    )


# =====================================================
# SEND OTP EMAIL
# =====================================================

def send_otp_email(
    receiver_email,
    otp
):
    """
    Sends OTP to user's email address securely.
    Returns: (success: bool, message: str)
    """

    # Validate credentials exist
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return False, "Email service not configured. Admin needs to set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."

    subject = "PrepNexus Login OTP Verification"

    body = f"""
Your OTP for PrepNexus login is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this login, please ignore this email.

- PrepNexus Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    try:
        # =================================================
        # TRY GMAIL SMTP WITH EXTENDED TIMEOUT
        # =================================================
        print(f"Attempting to send OTP to {receiver_email}...")
        
        # Use socket timeout for more reliable connection handling
        socket.setdefaulttimeout(20)
        
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=20
        ) as server:
            # Set debug level for better error tracking
            server.set_debuglevel(0)
            
            print(f"Connected to SMTP server. Logging in as {EMAIL_ADDRESS}...")
            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            print(f"Login successful. Sending email...")
            server.sendmail(
                EMAIL_ADDRESS,
                receiver_email,
                msg.as_string()
            )

        print("Email sent successfully!")
        return True, "OTP sent successfully! Check your email."

    except smtplib.SMTPAuthenticationError as auth_error:
        error_msg = f"Authentication failed: {str(auth_error)}"
        print(f"SMTP Auth Error: {error_msg}")
        return False, "Gmail credentials are incorrect. Please check EMAIL_ADDRESS and EMAIL_PASSWORD in .env file and ensure 2FA is enabled with App Password."

    except smtplib.SMTPServerDisconnected as disconnect_error:
        error_msg = f"Server disconnected: {str(disconnect_error)}"
        print(f"SMTP Disconnect Error: {error_msg}")
        return False, "Gmail server disconnected. Please try again in a moment."

    except socket.timeout:
        error_msg = "Connection timeout"
        print(f"Socket Timeout: {error_msg}")
        return False, "Connection timeout. Please check your internet connection and try again."

    except smtplib.SMTPException as smtp_error:
        error_msg = f"SMTP Error: {str(smtp_error)}"
        print(error_msg)
        return False, error_msg

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)
        return False, error_msg
    
    finally:
        # Reset socket timeout to default
        socket.setdefaulttimeout(None)