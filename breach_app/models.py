from django.contrib.auth.models import User
from django.db import models

class RedeemCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_redeemed = models.BooleanField(default=False)
    code_type = models.CharField(max_length=10, choices=[('5', '5'), ('10', '10'), ('15', '15')])

    def __str__(self):
        return self.code


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    search_limit = models.IntegerField(default=3)
    search_count = models.IntegerField(default=0)
    redeem_code = models.CharField(max_length=50, blank=True)
    redeem_code_type = models.CharField(max_length=10, blank=True)
    redeemed_codes = models.ManyToManyField(RedeemCode, blank=True)
    premium_search_count = models.IntegerField(default=0)
    premium_search_used = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    def decrease_search_count(self):
        if self.is_premium and self.premium_search_count > 0:
            self.premium_search_count -= 1
        elif not self.is_premium and self.search_count > 0:
            self.search_count -= 1
