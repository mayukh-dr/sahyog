from django.db import models
from datetime import date 
from django.urls import reverse 
from django.contrib.auth import get_user_model

# Create your models here.


class Airport(models.Model):
    iata_code = models.CharField(max_length=3)
    airport_name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    country_iso_alpha2 = models.CharField(max_length=2)
    timezone = models.CharField(max_length=32)
    time_offset = models.CharField(max_length=32)
    longitude = models.DecimalField(max_digits=13, decimal_places = 10)
    latitude = models.DecimalField(max_digits=12, decimal_places = 10)
    
    def __str__(self):
        return self.iata_code
    
class Post(models.Model):
    flight_number = models.CharField(max_length=32)
    travel_date = models.DateField(default=date.today)
    origin = models.ForeignKey(Airport, on_delete = models.PROTECT, related_name='origin', null=True)
    destination = models.ForeignKey(Airport, on_delete = models.PROTECT, related_name='destination', null=True)
    message = models.TextField(max_length=512)
    traveler = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
    def __str__(self):
        return f"Flight Number : {self.flight_number} | Travel Date : {self.travel_date}"
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=512)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete = models.PROTECT
    )
    
    def __str__(self):
        return self.comment
        
    def get_absolute_url(self):
        return reverse('post_list')
    
