from django.urls import path
from welcomeapp import views

app_name = 'welcomeapp'
urlpatterns = [
    path('content_page/', views.content_page, name='mainpage'),
    path('feedback/', views.feedback, name='feedback'),
    path('api/channels/', views.api_channels, name='api_channels'),
    path('proxy/', views.proxy_stream, name='proxy_stream'),
]
