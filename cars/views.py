from django import template
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify

from .models import Car, CarImage, CarInquiry, CarMake, CarModel
from .forms import CarForm, CarImageFormSet, CarInquiryForm, CarFilterForm

register = template.Library()


class HomeView(ListView):
    model = Car
    template_name = 'home.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Car.objects.filter(is_featured=True, is_sold=False)[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_cars'] = Car.objects.filter(car_type=Car.NEW, is_sold=False)[:3]
        context['reconditioned_cars'] = Car.objects.filter(car_type=Car.RECONDITIONED, is_sold=False)[:3]
        context['makes'] = CarMake.objects.all()
        return context

def home(request):
    context = {
        'makes': CarMake.objects.all(),
        'featured_cars': Car.objects.filter(is_featured=True, is_sold=False)[:6],
        'new_cars': Car.objects.filter(car_type='new', is_sold=False)[:6],
        'reconditioned_cars': Car.objects.filter(car_type='reconditioned', is_sold=False)[:6],
        'featured_car': Car.objects.filter(is_featured=True, is_sold=False).first(),
    }
    return render(request, 'home.html', context)


class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        queryset = Car.objects.filter(is_sold=False)

        # Apply filters
        form = CarFilterForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('make'):
                queryset = queryset.filter(make__name__icontains=data['make'])

            if data.get('model'):
                queryset = queryset.filter(model__name__icontains=data['model'])

            if data.get('car_type'):
                queryset = queryset.filter(car_type=data['car_type'])

            if data.get('min_price'):
                queryset = queryset.filter(price__gte=data['min_price'])

            if data.get('max_price'):
                queryset = queryset.filter(price__lte=data['max_price'])

            if data.get('min_year'):
                queryset = queryset.filter(year__gte=data['min_year'])

            if data.get('max_year'):
                queryset = queryset.filter(year__lte=data['max_year'])

            if data.get('transmission'):
                queryset = queryset.filter(transmission=data['transmission'])

            if data.get('fuel_type'):
                queryset = queryset.filter(fuel_type=data['fuel_type'])

        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(make__name__icontains=q) |
                Q(model__name__icontains=q) |
                Q(description__icontains=q) |
                Q(features__icontains=q)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CarFilterForm(self.request.GET)
        context['car_types'] = Car.CAR_TYPE_CHOICES
        context['makes'] = CarMake.objects.all()
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry_form'] = CarInquiryForm()
        context['similar_cars'] = Car.objects.filter(
            make=self.object.make,
            is_sold=False
        ).exclude(id=self.object.id)[:3]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CarInquiryForm(request.POST)

        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.car = self.object
            inquiry.save()
            messages.success(request, "Your inquiry has been sent successfully!")
            return redirect('car-detail', slug=self.object.slug)

        context = self.get_context_data(inquiry_form=form)
        return self.render_to_response(context)


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'cars/car_form.html'

    def form_valid(self, form):
        form.instance.seller = self.request.user

        # Generate slug
        base_slug = slugify(f"{form.instance.year} {form.instance.make} {form.instance.model}")
        slug = base_slug
        counter = 1

        while Car.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        form.instance.slug = slug

        # Save the car first
        response = super().form_valid(form)

        # Then handle the images
        formset = CarImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()

        messages.success(self.request, "Car listing created successfully!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = CarImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = CarImageFormSet()

        return context


class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'cars/car_form.html'

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.seller

    def form_valid(self, form):
        response = super().form_valid(form)

        # Handle the images
        formset = CarImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()

        messages.success(self.request, "Car listing updated successfully!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = CarImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['formset'] = CarImageFormSet(instance=self.object)

        return context


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('my-listings')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.seller


@login_required
def mark_as_sold(request, slug):
    car = get_object_or_404(Car, slug=slug)

    if request.user != car.seller:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('car-detail', slug=slug)

    car.is_sold = True
    car.save()
    messages.success(request, "Car marked as sold successfully!")
    return redirect('my-listings')


@login_required
def my_listings(request):
    cars = Car.objects.filter(seller=request.user)
    return render(request, 'cars/my_listings.html', {'cars': cars})


@login_required
def my_inquiries(request):
    cars = Car.objects.filter(seller=request.user)
    inquiries = CarInquiry.objects.filter(car__in=cars).order_by('-created_at')
    return render(request, 'cars/my_inquiries.html', {'inquiries': inquiries})


@login_required
def mark_inquiry_responded(request, pk):
    inquiry = get_object_or_404(CarInquiry, pk=pk)

    if request.user != inquiry.car.seller:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('my-inquiries')

    inquiry.responded = not inquiry.responded
    inquiry.save()

    status = "responded to" if inquiry.responded else "not responded to"
    messages.success(request, f"Inquiry marked as {status}.")
    return redirect('my-inquiries')