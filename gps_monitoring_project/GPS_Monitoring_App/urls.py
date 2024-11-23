from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView




urlpatterns = [
    path('login/', LoginView.as_view(template_name='TemplatesBase/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', RedirectView.as_view(url= 'login/', permanent =False)),
    path('home/', views.home, name='home'),
    path('monitoring/', views.monitoring_view, name='monitoring'),
    path('Reportes/', views.Reportes, name='Reportes'),
    path('Arrendatarios/', views.Arrendatarios, name='arrendatario'),
    path('api/vehiculo-ubicacion/', views.obtener_ubicacion_vehiculo, name='ubicacion_vehiculo'),
    path("vehiculos/", views.obtener_modelos_y_vehiculos, name="vehiculos"),
    path('vehiculos/registrar/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('login/', views.login, name='login'),

]


