from django.contrib import admin
from .models import Car, CarMake, CarModel, CarImage, CarInquiry


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 2


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make')
    list_filter = ('make',)
    search_fields = ('name', 'make__name')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'car_type', 'price', 'is_sold', 'is_featured', 'posted_on')
    list_filter = ('car_type', 'make', 'is_sold', 'is_featured', 'transmission', 'fuel_type')
    search_fields = ('make__name', 'model__name', 'description', 'features')
    readonly_fields = ('posted_on', 'updated_on')
    prepopulated_fields = {'slug': ('year', 'make', 'model')}
    inlines = [CarImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('make', 'model', 'year', 'car_type', 'price', 'slug')
        }),
        ('Technical Specifications', {
            'fields': ('mileage', 'engine_capacity', 'transmission', 'fuel_type', 'color', 'doors', 'seats')
        }),
        ('Features and Description', {
            'fields': ('features', 'description')
        }),
        ('Recondition Information', {
            'fields': ('country_of_origin', 'recondition_status'),
            'classes': ('collapse',)
        }),
        ('Sales Information', {
            'fields': ('seller', 'is_featured', 'is_sold', 'posted_on', 'updated_on')
        }),
    )


@admin.register(CarInquiry)
class CarInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'email', 'phone', 'created_at', 'responded')
    list_filter = ('responded', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'car__make__name', 'car__model__name')
    readonly_fields = ('created_at',)