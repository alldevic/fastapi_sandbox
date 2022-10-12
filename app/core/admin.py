"""
Amis Admin configuration
"""

from fastapi_amis_admin.admin import admin

from .models import Song


class SongsAdmin(admin.ModelAdmin):
    """
    Song admin interface
    """
    page_schema = 'Songs'
    model = Song
