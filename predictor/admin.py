from django.contrib import admin
from .models import PredictionRecord


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "risk_level", "probability", "created_at")
    list_filter = ("risk_level", "gender", "created_at")
    search_fields = ("name",)
