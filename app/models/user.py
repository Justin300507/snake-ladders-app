from app.models.users import Users

# Alias so that `from app.models.user import User` works everywhere
User = Users

__all__ = ["User"]
