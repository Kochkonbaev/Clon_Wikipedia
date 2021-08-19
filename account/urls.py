from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='dashboard'),
    # path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', views.logout_view, name='logout'),
]
