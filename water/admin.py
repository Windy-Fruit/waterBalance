from django.contrib import admin
from .models import UserProfile, DailyWaterNorm, WaterIntake

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "weight", "height", "activity_level", "climate")
    search_fields = ("user__username",)


@admin.register(DailyWaterNorm)
class DailyWaterNormAdmin(admin.ModelAdmin):
    list_display = ("user", "calculated_norm", "date_created")
    list_filter = ("date_created",)


@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "intake_time", "date")
    list_filter = ("date",)
    search_fields = ("user__username",)
