import os
import random
import smtplib
import socket
from email.mime.text import MIMEText
from dotenv import load_dotenv


# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# =====================================================
# LOAD .ENV FILE
# =====================================================

env_path = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    dotenv_path=env_path,
    override=True
)


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

    return str(
        random.randint(
            100000,
            999999
        )
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