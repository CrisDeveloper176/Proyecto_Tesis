from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .Views.vehiculos import *
from .Views.arrendatarios import *
from .Views.login import *
from .Views.monitoreo import *
from .Views.reportes import *




urlpatterns = [
    path('login/', LoginView.as_view(template_name='TemplatesBase/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', RedirectView.as_view(url= 'login/', permanent =False)),
    path('home/', home, name='home'),
    path('monitoring/', monitoring_view, name='monitoring'),
    path('Reportes/', Reportes, name='Reportes'),
    path('Arrendatarios/', obtener_arrendatarios, name='arrendatario'),
    path('Arrendatarios/Registrar', registrar_arrendatario, name='registrar_arrendatario'),
    path('Arrendatarios/Editar/<int:id>/', editar_arrendatario, name='editar_arrendatario'),
    path('Arrendatarios/Eliminar/<int:id>/', eliminar_arrendatario, name='eliminar_arrendatario'),
    path("vehiculos/", obtener_modelos_y_vehiculos, name="vehiculos"),
    path('vehiculos/Registrar', registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/Editar/<int:ID_Vehiculo>/', editar_vehiculo , name='editar_Vehiculo'),
    path('vehiculos/Eliminar/<int:ID_Vehiculo>/', eliminar_vehiculo, name='eliminar_Vehiculo'),
    path('login/', login, name='login'),

]


