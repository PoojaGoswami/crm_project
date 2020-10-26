from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    athlete_code = models.CharField(max_length=128, unique=True,)
    birth_date = models.DateField(max_length=50, blank=True)
    address = models.TextField(max_length=500, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    failed_attempt = models.IntegerField(default=0)


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', )

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
