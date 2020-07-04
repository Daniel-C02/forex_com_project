import sys
from PIL import Image
from io import BytesIO
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField
from datetime import date
import datetime
from django.utils import timezone

def validate_image(image):
    file_size = image.file.size
    limit_kb = 3000
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

class Trade(models.Model):
    FOREXPAIRS_CHOICES = (
        ("EUR_USD" , "EUR_USD"),
        ("GBP_USD" , "GBP_USD"),
        ("USD_JPY" , "USD_JPY"),
        ("AUD_USD" , "AUD_USD"),
        ("NZD_USD" , "NZD_USD"),
        ("USD_CAD" , "USD_CAD"),
        ("USD_CHF" , "USD_CHF"),
        ("EUR_GBP" , "EUR_GBP"),
        ("GBP_JPY" , "GBP_JPY"),
        ("AUD_GBP" , "AUD_GBP"),
        ("GBP_NZD" , "GBP_NZD"),
        ("GBP_CAD" , "GBP_CAD"),
        ("GBP_CHF" , "GBP_CHF"),
        ("EUR_JPY" , "EUR_JPY"),
        ("EUR_AUD" , "EUR_AUD"),
        ("EUR_NZD" , "EUR_NZD"),
        ("EUR_CAD" , "EUR_CAD"),
        ("EUR_CHF" , "EUR_CHF"),
        ("AUD_JPY" , "AUD_JPY"),
        ("AUD_NZD" , "AUD_NZD"),
        ("AUD_CAD" , "AUD_CAD"),
        ("AUD_CHF" , "AUD_CHF"),
        ("CAD_JPY" , "CAD_JPY"),
        ("NZD_CAD" , "NZD_CAD"),
        ("CAD_CHF" , "CAD_CHF"),
        ("NZD_JPY" , "NZD_JPY"),
        ("NZD_CHF" , "NZD_CHF"),
        ("CHF_JPY" , "CHF_JPY"),
        ("XAU_USD" , "XAU_USD"),
        ("XBT_USD" , "XBT_USD"),
        ("XNG_USD" , "XNG_USD"),
        ("XTI_USD" , "XTI_USD"),
        ("BTC_USD" , "BTC_USD"),
    )
    WL_CHOICES = (
        ('WIN', 'WIN'),
        ('LOSE', 'LOSE'),
        ('BE', 'BE'),
    )
    CURRENCY_CHOICES = (
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
    )
    pair = models.CharField(max_length=10, choices=FOREXPAIRS_CHOICES, default='EUR_USD')
    description = models.CharField(max_length=100, blank=True)
    pips = models.PositiveSmallIntegerField(default=1, blank=True, null=True, validators=[MaxValueValidator(5000)])
    amount = MoneyField(decimal_places=0, default_currency='USD', max_digits=7,currency_choices=CURRENCY_CHOICES, blank=True, null=True)
    winlose = models.CharField(max_length=4, choices=WL_CHOICES)
    lotsize = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(float('0.01'))])
    openedpositionon = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='images/trades/', validators=[validate_image])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Trade, self).save(*args, **kwargs)

    def compressImage(self,image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        basewidth = 520
        wpercent = (basewidth/float(imageTemproary.size[0]))
        hsize = int((float(imageTemproary.size[1])*float(wpercent)))
        imageTemproaryResized = imageTemproary.resize( (basewidth,hsize) )
        imageTemproaryResized.save(outputIoStream , format='png', quality=60)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" % image.name.split('.')[0], 'images/trades/png', sys.getsizeof(outputIoStream), None)
        return image

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    LEVEL_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
        ('ProTrader', 'ProTrader'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    authentic = models.BooleanField(default=False)
    traderlevel = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='Beginner')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male') 
    name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='images/userpfp/', validators=[validate_image], blank=True)
    bio = models.CharField(max_length=300, blank=True)
    country = CountryField(blank=True)
    instagram = models.URLField(blank=True)
    dateregistered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def compressImageMain(self,image):
        if self.image:

            def save(self, *args, **kwargs):
                if not self.id:
                    self.image = self.compressImage(self.image)
                super(UserProfile, self).save(*args, **kwargs)
            def compressImage(self,image):
                imageTemproary = Image.open(image)
                outputIoStream = BytesIO()
                basewidth = 520
                wpercent = (basewidth/float(imageTemproary.size[0]))
                hsize = int((float(imageTemproary.size[1])*float(wpercent)))
                imageTemproaryResized = imageTemproary.resize( (basewidth,hsize) )
                imageTemproaryResized.save(outputIoStream , format='PNG', quality=60)
                outputIoStream.seek(0)
                image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" % image.name.split('.')[0], 'images/userpfp/png', sys.getsizeof(outputIoStream), None)
                return image
        else:
            pass









