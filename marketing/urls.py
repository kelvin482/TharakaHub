from django.urls import path
from . import views


app_name = 'marketing'

urlpatterns = [
    path('', views.jobs_list, name='jobs_list'),
    path('jobs/', views.jobs_list, name='jobs_list_alt'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/proposal/', views.proposal_create, name='proposal_create'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


