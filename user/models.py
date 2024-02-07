from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class Mobile(models.Model):
    mobile = models.CharField(max_length=16)
    is_sms_sent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    sms_code = models.CharField(max_length=16, default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.mobile
    
    class Meta:
        ordering = ['-created_at']
    

class User(AbstractUser):
    is_driver = models.BooleanField(default=True, verbose_name="Водитель?")

    def save(self, *args, **kwargs):
        if not self.pk:
            super(User, self).save(*args, **kwargs)
            Profile.objects.create(user=self)
        else:
            super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Поьзователь')
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    mobile = models.CharField(max_length=64, blank=True, null=True, verbose_name='Мобильный')
    image = models.ImageField(("Фото"), upload_to = "profiles/", default="profiles/default.jpg")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    is_active = models.BooleanField(default=True, verbose_name="Активный?")
    is_avaliable = models.BooleanField(default=True, verbose_name="Рабочий?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"