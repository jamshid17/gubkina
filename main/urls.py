from django.urls import path
from .views import home_form_view, test


urlpatterns = [
    path('', home_form_view, name='main'),
    path('test', test, name='test')
]
