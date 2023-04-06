from django.urls import path
from . import views

urlpatterns = [
    # /
    path('', views.landing, name='landing'),
    # /about_me/
    path('aboutme/', views.about_me, name='aboutme'),
]