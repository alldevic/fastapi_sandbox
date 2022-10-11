"""
Customize and fix debug-toolbar issues
"""

from core.db import settings
from debug_toolbar.middleware import DebugToolbarMiddleware
from jinja2 import Environment

toolbar = {
    'middleware_class':DebugToolbarMiddleware,
    'panels':["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    'session_generators':["core.db:get_async_session"],
    'settings':[settings],
    'jinja_env':Environment()
}
