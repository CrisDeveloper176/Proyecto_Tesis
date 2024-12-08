from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .Views.vehiculos import *
from .Views.arrendatarios import *
from .Views.login import *
from .Views.monitoreo import *
from .Views.ReporteViaje import *
from .Views.ReporteVehiculo import *
from .Views.ReporteMantenimiento import *
from .Views.estado_dispositivo import *
from .Views.dispositivogps import *
from .Views.gpsusado import *
from .Views.HistorialVIaje import *
from .Views.registrarmodelos import *
<<<<<<< HEAD
=======

>>>>>>> 7127ca231e68a8fb1639be3b026eac2f30bbf6b6
from .Views.registrarmodelos import *





urlpatterns = [
    path('login/', LoginView.as_view(template_name='TemplatesBase/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', RedirectView.as_view(url= 'login/', permanent =False)),
    path('home/', home, name='home'),
    path('monitoring/', monitoring_view, name='monitoring'),
    path('HistorialViaje/', HistorialViaje_view, name='HistorialViaje'),
    path('reporte/obtener_vehiculos/', obtener_modelos_y_vehiculos_reporte, name='obtener_vehiculos'),
    path('Arrendatarios/', obtener_arrendatarios, name='arrendatario'),
    path('Arrendatarios/Registrar', registrar_arrendatario, name='registrar_arrendatario'),
    path('Arrendatarios/Editar/<str:rut>/', editar_arrendatario, name='editar_arrendatario'),
    path('Arrendatarios/Eliminar/<str:rut>/', eliminar_arrendatario, name='eliminar_arrendatario'),
    path("vehiculos/", obtener_modelos_y_vehiculos, name="vehiculos"),
    path('vehiculos/Registrar', registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/Editar/<int:ID_Vehiculo>/', editar_vehiculo , name='editar_Vehiculo'),
    path('vehiculos/Eliminar/<int:ID_Vehiculo>/', eliminar_vehiculo, name='eliminar_Vehiculo'),

   # Estados GPS
    path('estadoGps/', listar_estados_gps, name='estadoGps'),
    path('estadoGps/Registrar/', registrar_estado_gps, name='registrar_estado_gps'),
    path('estadoGps/Editar/<int:ID_EstadoGps>/', editar_estado_gps, name='editar_estado_gps'),
    path('estadoGps/Eliminar/<int:ID_EstadoGps>/', eliminar_estado_gps, name='eliminar_estado_gps'),

    path('dispositivos/', listar_dispositivos_gps, name='dispositivoGps'),
    path('dispositivos/<int:ID_DispositivoGps>/estados/', obtener_estados_por_dispositivo, name='estadosPorDispositivo'),
    path('dispositivos/registrar/', registrar_dispositivo_gps, name='registrarDispositivoGps'),
    path('dispositivoGps/Editar/<slug:imei>/', editar_dispositivo_gps, name='editarDispositivoGps'),
    path('dispositivoGps/Eliminar/<slug:imei>/', eliminar_dispositivo_gps, name='eliminarDispositivoGps'),


    path('dispositivos_usados/', listar_dispositivos_gps_usados, name='gpsusado'),
    path('dispositivos_usados/registrar/', registrar_dispositivo_gps_usado, name='registrarGpsUsado'),
    path('dispositivos_usados/editar/<str:imei>/', editar_dispositivo_gps_usado, name='editarGpsUsado'),

    


    path('modelos-marcas/', obtener_modelos_y_marcas, name='modelos_marcas'),
    path('modelos-marcas/registrar-modelo/', registrar_modelo, name='registrar_modelo'),
    path('modelos-marcas/editar-modelo/<int:ID_Modelo>/', editar_modelo, name='editar_modelo'),
    path('modelos-marcas/eliminar-modelo/<int:ID_Modelo>/', eliminar_modelo, name='eliminar_modelo'),
    path('modelos-marcas/registrar-marca/', registrar_marca, name='registrar_marca'),
   




    path('ReporteViaje/', obtener_viajes, name='ReporteViaje'),
    path('ReporteVehiculo/', Reporte_Vehiculo , name='ReporteVehiculo'),
    path('login/', login, name='login'),
]


