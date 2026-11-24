from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='Aboutus'),
    path('features/', views.features, name='Features'),
    path('events/', views.events, name='Events'),
    path('howitworks/', views.howitworks, name='HowItWorks'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('createanevent/', views.createanevent, name='createanevent'),
    path('enterpriseeventdashboard/', views.enterpriseeventdashboard, name='enterpriseeventdashboard'),
]