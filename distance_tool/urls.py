from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_address, name='add_address'),
    path('edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path('show_distances/', views.show_distances, name='show_distances'),
]
