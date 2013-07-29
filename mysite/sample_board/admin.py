from django.contrib import admin
from sample_board.models import DjangoBoard
from sample_board.models import Settings

class SettingsAdmin(admin.ModelAdmin):
	model = Settings

admin.site.register(DjangoBoard, SettingsAdmin)