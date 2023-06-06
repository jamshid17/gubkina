from django.urls import path
from .views import home_form_view


urlpatterns = [
    path('', home_form_view, name='main'),
]
