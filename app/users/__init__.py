"""
Users and auth module
"""
from .db import get_user_db as get_user_db
from .routes import routes as users_routes
from .users import current_active_user as current_active_user
