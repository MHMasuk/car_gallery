from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarListView.as_view(), name='car-list'),
    path('new/', views.CarListView.as_view(), {'car_type': 'new'}, name='new-cars'),
    path('reconditioned/', views.CarListView.as_view(), {'car_type': 'reconditioned'}, name='reconditioned-cars'),
    path('add/', views.CarCreateView.as_view(), name='car-create'),
    path('<slug:slug>/', views.CarDetailView.as_view(), name='car-detail'),
    path('<slug:slug>/update/', views.CarUpdateView.as_view(), name='car-update'),
    path('<slug:slug>/delete/', views.CarDeleteView.as_view(), name='car-delete'),
    path('<slug:slug>/mark-sold/', views.mark_as_sold, name='mark-as-sold'),
    path('my/listings/', views.my_listings, name='my-listings'),
    path('my/inquiries/', views.my_inquiries, name='my-inquiries'),
    path('inquiry/<int:pk>/mark-responded/', views.mark_inquiry_responded, name='mark-inquiry-responded'),
]