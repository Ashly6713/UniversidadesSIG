from django.urls import path
from .views import (
    public_map_view,
    calificar,
    universidad_list,
    universidad_create_edit,
    universidad_delete,
    facultad_list,
    facultad_create_edit,
    facultad_delete,
    carrera_list,
    carrera_create_edit,
    carrera_delete,
    top_items_view,
    toggle_favorito,
    favoritos_list,
    register
)

urlpatterns = [
     path('', public_map_view, name='home'),

     path('register/', register, name='register'),
     path('calificar/', calificar, name='calificar'),

    path('universidades/', universidad_list, name='universidad_list'),
    path('universidades/nueva/', universidad_create_edit, name='universidad_create'),
    path('universidades/editar/<int:pk>/', universidad_create_edit, name='universidad_edit'),
    path('universidades/eliminar/<int:pk>/', universidad_delete, name='universidad_delete'),

     path('facultades/', facultad_list, name='facultad_list'),
    path('facultades/nueva/', facultad_create_edit, name='facultad_create'),
    path('facultades/editar/<int:pk>/', facultad_create_edit, name='facultad_edit'),
    path('facultades/eliminar/<int:pk>/', facultad_delete, name='facultad_delete'),

    path('carreras/', carrera_list, name='carrera_list'),
    path('carreras/nueva/', carrera_create_edit, name='carrera_create'),
    path('carreras/editar/<int:pk>/', carrera_create_edit, name='carrera_edit'),
    path('carreras/eliminar/<int:pk>/', carrera_delete, name='carrera_delete'),

     path('top-items/', top_items_view, name='top_items'),
     path('toggle_favorito/', toggle_favorito, name='toggle_favorito'),
     path('favorito/', favoritos_list, name='favoritos_list'),





]
