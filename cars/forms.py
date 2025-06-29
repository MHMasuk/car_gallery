from django import forms
from .models import Car, CarInquiry, CarImage


class CarFilterForm(forms.Form):
    make = forms.CharField(required=False)
    model = forms.CharField(required=False)
    car_type = forms.ChoiceField(
        choices=[('', 'All')] + list(Car.CAR_TYPE_CHOICES),
        required=False
    )
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    min_year = forms.IntegerField(required=False)
    max_year = forms.IntegerField(required=False)
    transmission = forms.ChoiceField(
        choices=[('', 'All')] + list(Car.TRANSMISSION_CHOICES),
        required=False
    )
    fuel_type = forms.ChoiceField(
        choices=[('', 'All')] + list(Car.FUEL_TYPE_CHOICES),
        required=False
    )


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['seller', 'is_featured', 'is_sold', 'posted_on', 'updated_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields not required for New cars
        if self.data.get('car_type') == Car.NEW:
            self.fields['mileage'].required = False
            self.fields['country_of_origin'].required = False
            self.fields['recondition_status'].required = False


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image', 'is_primary']


CarImageFormSet = forms.inlineformset_factory(
    Car, CarImage,
    form=CarImageForm,
    extra=5,
    can_delete=True
)

from django import forms
from .models import CarInquiry


class CarInquiryForm(forms.ModelForm):
    """
    Form for car inquiries with Bootstrap styling applied directly
    """

    # Override fields to add Bootstrap classes
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'})
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'I am interested in this car. Please contact me with more information.'
        })
    )

    class Meta:
        model = CarInquiry
        fields = ['name', 'email', 'phone', 'message']
