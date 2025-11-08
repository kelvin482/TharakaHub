from django.urls import path
from . import views

app_name = "agent"

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('plot/', views.plot_view, name='plot'),
]
