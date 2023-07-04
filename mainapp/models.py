from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    action_timestamp = models.DateTimeField(auto_now_add=True)

    ACTION_CHOICES = (
        ('Like', 'Like'),
        ('Dislike', 'Dislike'),
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.action} - {self.image.name} - {self.action_timestamp}'
    
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)