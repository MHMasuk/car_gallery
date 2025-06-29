# Add to cars/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import CustomLoginView

urlpatterns = [
    # ... your existing URLs
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

]