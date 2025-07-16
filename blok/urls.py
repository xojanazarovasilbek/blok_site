from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>', category, name='categor'),
    path('detail/<int:pk>', new_detail, name='detail'),
    path('profile/', profile, name='profile')
]