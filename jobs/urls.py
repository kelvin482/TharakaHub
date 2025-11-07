from django.urls import path
from . import views


app_name = 'jobs'


urlpatterns = [
    path('create/', views.create_job, name='create'),
    path('', views.job_list, name='list'),
    path('<int:pk>/', views.job_detail, name='detail'),
    #applying for the job
    path('<int:job_id>/apply/', views.apply_job, name='apply'),
    

    #change application status (creator accepts/declines)
     path('application/<int:app_id>/<str:new_status>/', views.change_application_status, name='change_application_status'),



]

