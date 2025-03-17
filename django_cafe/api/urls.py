from django.urls import path
from api import views

urlpatterns = [
    path('auth/register/', views.create_user, name='register')
]
