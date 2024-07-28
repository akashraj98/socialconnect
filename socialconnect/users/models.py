from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    profile_url = models.URLField(blank=True, null=True)

    def user_deactivate(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.username
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower} follows {self.followed}'

