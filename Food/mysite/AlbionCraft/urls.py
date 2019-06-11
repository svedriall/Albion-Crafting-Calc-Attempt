from django.urls import path
from . import views
app_name = 'AlbionCraft'
urlpatterns = [
    path('', views.data_list, name='data_list'),
    path('requirement', views.requirement_list, name='requirement_list'),
]