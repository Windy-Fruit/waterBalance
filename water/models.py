from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.IntegerField()
    activity_level = models.CharField(max_length=20)
    climate = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
    
class DailyWaterNorm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calculated_norm = models.FloatField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def calculate_norm(self):
        profile = UserProfile.objects.get(user=self.user)
        base = profile.weight * 30

        activity_map = {
            'low': 1.0,
            'medium': 1.2,
            'high': 1.4,
        }

        climate_map = {
            'cold': 1.0,
            'normal': 1.1,
            'hot': 1.2,
        }

        activity_coef = activity_map.get(profile.activity_level, 1)
        climate_coef = climate_map.get(profile.climate, 1)

        return base * activity_coef * climate_coef

    def save(self, *args, **kwargs):
        if not self.calculated_norm:
            self.calculated_norm = self.calculate_norm()
        super().save(*args, **kwargs)

    def get_today_intake(self):
        today = timezone.now().date()
        total = WaterIntake.objects.filter(
            user=self.user,
            date=today
        ).aggregate(Sum('amount'))['amount__sum']

        return total or 0

    def get_progress_percent(self):
        if not self.calculated_norm:
            return 0
        return round((self.get_today_intake() / self.calculated_norm) * 100, 1)

    def __str__(self):
        return f"{self.user.username} - {self.calculated_norm:.0f} ml"
        
class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    intake_time = models.DateTimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.amount} ml"
