from django.urls import path
from . import views  


urlpatterns = [

     path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('crear-vehiculo/', views.create_vehiculo, name='create_vehiculo'),
    path('vehiculos/', views.get_vehiculo_by_id, name='get_vehiculos'),
    path('vehiculos/<int:vehiculo_id>/', views.get_vehiculo_by_id, name='get_vehiculo_by_id'),
    path('actualizar-vehiculo/<int:vehiculo_id>/', views.update_vehiculo, name='update_vehiculo'),
    path('eliminar-vehiculo/<int:vehiculo_id>/', views.delete_vehiculo, name='delete_vehiculo'),
    
]