from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView




urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', RedirectView.as_view(url= 'login', permanent =False)),
    path('home/', views.home, name='home'),
    path('Vehiculos/', views.vehiculos, name='Vehiculos'),
    path('monitoring/', views.monitoring_view, name='monitoring'),
    path('Reportes/', views.Reportes, name='Reportes'),
    path('Arrendatarios/', views.Arrendatarios, name='arrendatarios'),
    path('api/vehiculo-ubicacion/', views.obtener_ubicacion_vehiculo, name='ubicacion_vehiculo'),
    #path('crear-arrendatario/', views.crear_arrendatario, name='crear_arrendatario'),
]

