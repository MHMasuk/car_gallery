from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='makes/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.make.name} {self.name}"


class Car(models.Model):
    # Car type choices
    NEW = 'new'
    RECONDITIONED = 'reconditioned'
    USED = 'used'

    CAR_TYPE_CHOICES = [
        (NEW, 'New'),
        (RECONDITIONED, 'Reconditioned'),
        (USED, 'Used')
    ]

    # Transmission choices
    AUTOMATIC = 'automatic'
    MANUAL = 'manual'
    CVT = 'cvt'

    TRANSMISSION_CHOICES = [
        (AUTOMATIC, 'Automatic'),
        (MANUAL, 'Manual'),
        (CVT, 'CVT')
    ]

    # Fuel type choices
    PETROL = 'petrol'
    DIESEL = 'diesel'
    HYBRID = 'hybrid'
    ELECTRIC = 'electric'

    FUEL_TYPE_CHOICES = [
        (PETROL, 'Petrol'),
        (DIESEL, 'Diesel'),
        (HYBRID, 'Hybrid'),
        (ELECTRIC, 'Electric')
    ]

    # Basic info
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='cars')
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='cars')
    year = models.PositiveIntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField(help_text="Mileage in km")

    # Technical specs
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=1, help_text="Engine capacity in liters")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    color = models.CharField(max_length=50)
    doors = models.PositiveSmallIntegerField(default=4)
    seats = models.PositiveSmallIntegerField(default=5)

    # Features and description
    features = models.TextField(help_text="List the features of the car")
    description = models.TextField()

    # Reconditioned specific fields
    country_of_origin = models.CharField(max_length=100, blank=True, null=True)
    recondition_status = models.CharField(max_length=100, blank=True, null=True,
                                          help_text="Details about reconditioning work done")

    # Sales info
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # SEO
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.get_car_type_display()}"

    def get_absolute_url(self):
        return reverse('car-detail', kwargs={'slug': self.slug})


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.car}"


class CarInquiry(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Car Inquiries"

    def __str__(self):
        return f"Inquiry from {self.name} about {self.car}"