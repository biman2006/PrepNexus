import os

class AdminAuth:
    @staticmethod
    def login(username, password):
        def get_env_value(key):
            value = os.getenv(key)
            if isinstance(value, str):
                value = value.strip()
                return value if value else None
            return value

        admin_username = get_env_value("ADMIN_NAME")
        admin_password = get_env_value("ADMIN_PASSWORD")

        if not admin_username or not admin_password:
            return False

        return username == admin_username and password == admin_password

    


