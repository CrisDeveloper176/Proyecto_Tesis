from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
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
from .Views.RegistrarMarca import *
from .Views.RegistrarModelo import *
from .Views.TipoAlerta import *
from .Views.Alertas import *
from .Views.RegistrarVehiculo import *





urlpatterns = [
    path('login/', LoginView.as_view(template_name='TemplatesBase/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', RedirectView.as_view(url= 'login/', permanent =False)),
    path('home/', home, name='home'),
    path('monitoring/', monitoring_view, name='monitoring'),
    path('TipoAlerta/', TipoAlerta_view , name='TipoAlerta'),
    path('Alerta/', Alerta_view , name='Alerta'),
    path('HistorialViaje/', HistorialViaje_view, name='HistorialViaje'),
    path('reporte/obtener_vehiculos/', obtener_modelos_y_vehiculos_reporte, name='obtener_vehiculos'),
    path('Arrendatarios/', obtener_arrendatarios, name='arrendatario'),
    path('Arrendatarios/Registrar', registrar_arrendatario, name='registrar_arrendatario'),
    path('Arrendatarios/Editar/<str:rut>/', editar_arrendatario, name='editar_arrendatario'),
    path('Arrendatarios/Eliminar/<str:rut>/', eliminar_arrendatario, name='eliminar_arrendatario'),
 

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

    

    path('registrar-marca/', visualizar_marca, name='registrar_marca'),
    path('registrar-modelo/', visualizar_modelo, name='registrar_modelo'),
    path('registrar-vehiculo/', visualizar_vehiculo, name='registrar_vehiculo'),
   






    path('ReporteViaje/', obtener_viajes, name='ReporteViaje'),
    path('ReporteVehiculo/', Reporte_Vehiculo , name='ReporteVehiculo'),
    path('login/', login, name='login'),
]


