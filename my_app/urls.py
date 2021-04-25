from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('search',views.new_search,name='search'),
]