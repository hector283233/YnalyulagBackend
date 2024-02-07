from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User, Profile

class Transport(models.Model):
    VEHICLE_TYPE = [
        ("Ýolagçy awtoulag", "Ýolagçy awtoulag"),
        ("Ýük awtoulag", "Ýük awtoulag"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="user_transport",
                                verbose_name="Пользоатель")
    model = models.CharField(max_length=255, verbose_name="Модель автомобиля")
    vehicle_type = models.CharField(max_length=255, choices=VEHICLE_TYPE,
                                    default="Ýolagçy awtoulag")
    image = models.ImageField(upload_to="transports/", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.user) + ' - ' + str(self.model)
    
    class Meta:
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорты"
        
class Locations(models.Model):
    REGIONS = [
        ("Aşgabat", "Aşgabat"),
        ("Mary", "Mary"),
        ("Lebap", "Lebap"),
        ("Daşoguz", "Daşoguz"),
        ("Balkan", "Balkan"),
        ("Ahal", "Ahal"),
    ]
    title = models.CharField(max_length=255, verbose_name="Город")
    region = models.CharField(max_length=16, choices=REGIONS, default="Aşgabat")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        
class Trip(models.Model):
    is_active = models.BooleanField(default=True)
    from_location = models.ForeignKey(Locations, on_delete=models.CASCADE,
                                      related_name="trip_from_location",
                                      verbose_name="Поездка из")
    to_location = models.ForeignKey(Locations, on_delete=models.CASCADE,
                                    related_name="trip_to_location",
                                    verbose_name="Поездка в")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="user_trip",
                                verbose_name="Профиль")
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE,
                                     related_name="trip_transport",
                                     verbose_name="Транспорт")
    leaving_time = models.DateTimeField(blank=True, null=True, 
                                        auto_now=False, auto_now_add=False,
                                        verbose_name="Время")
    capacity = models.IntegerField(default=4, blank=True, null=True,
                                   verbose_name="Число Людей")
    is_intercity = models.BooleanField(default=False, verbose_name="Внутригородний")
    is_onway = models.BooleanField(default=False, verbose_name="Попутный")
    description = models.CharField(max_length=255, verbose_name="Доп инфо",
                                    blank=True, null=True)
    cargo = models.BooleanField(default=False)
    passanger = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user) + ' - ' + str(self.to_location)
    
    class Meta:
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"
    
class Comments(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=255, verbose_name="Титул")
    detail = models.TextField(blank=True, null=True, verbose_name="Подробнее")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_comment',
                             verbose_name='Пользователь')
    user_commented = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="user_commented_comments",
                                verbose_name="Профиль")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user) + ' - ' + str(self.title)
    
    class Meta:
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"