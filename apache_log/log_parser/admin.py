from django.contrib import admin
from .models import LogData


class LogDataSitesAdmin(admin.ModelAdmin):
    list_display = ("pk", "ip", "date", "http_method", "url", "response_code", "response_size")
    search_fields = ( "ip", "date", "http_method", "url", "response_code", "response_size")
    empty_value_display = '-empty-'


admin.site.register(LogData, LogDataSitesAdmin)