from django.db import models
from django.contrib.auth.models import User


from django.db import models
from breach_app.models import RedeemCode

class AdminModel(models.Model):
    redeem_code = models.ForeignKey(RedeemCode, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    # Other fields for AdminModel
    ...


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username


