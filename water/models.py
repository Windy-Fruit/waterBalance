from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.IntegerField()
    activity_level = models.CharField(max_length=50)
    climate = models.CharField(max_length=50)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
class DailyWaterNorm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calculated_norm = models.FloatField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Water norm for {self.user.username}"
    
class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(help_text="Amount of water in ml")
    intake_time = models.DateTimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.amount} ml - {self.user.username}"
