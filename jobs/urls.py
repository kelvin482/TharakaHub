from django.urls import path
from . import views


app_name = 'jobs'


urlpatterns = [
    path('create/', views.create_job, name='create'),
    path('', views.job_list, name='list'),
    path('<int:pk>/', views.job_detail, name='detail'),
]

