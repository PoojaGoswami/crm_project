from django.db import models

# Create your models here.
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# class User(AbstractUser):
#     birth_date = models.DateField(max_length=50, null=True, blank=True)
#     address = models.TextField()
#     mobile = models.IntegerField(null=True, blank=True)
#     failed_attempt = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    athlete_code = models.CharField(max_length=128, unique=True)
    birth_date = models.DateField(max_length=50, null=True, blank=True)
    address = models.TextField()
    mobile = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    failed_attempt = models.IntegerField(default=0)
    # signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
