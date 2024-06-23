from django.db import models

# Create your models here.
class User(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    user_hash = models.CharField(null=False, blank=False, unique=True, max_length=64)
    username = models.CharField(null=False, blank=False, unique=True, max_length=64)
    password = models.CharField(null=False, blank=False, max_length=64)
    email = models.CharField(null=False, blank=False, max_length=64)
    first_name = models.CharField(null=False, blank=False, max_length=64)
    last_name = models.CharField(null=False, blank=False, max_length=64)
    role = models.IntegerField(null=False, blank=False, default=1) # 0 = admin, 1 = user
    creation_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(blank=True, null=True)
    # organization

    # def __str__(self):
    #     return f"{self.username} | {self.first_name} {self.last_name} | {self.organization}"