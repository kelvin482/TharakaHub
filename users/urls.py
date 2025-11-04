from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.jobs, name='jobs'),
    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    #paths in the dashboard
        path('projects/', views.projects, name='projects'),
    path('clients/', views.clients, name='clients'),
    path('messages/', views.messages_view, name='messages'),
    path('earnings/', views.earnings, name='earnings'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('settings/', views.settings, name='settings'),

    #projects
    path('dashboard/projects/', views.projects_view, name='projects'),
    path('dashboard/clients/', views.clients_view, name='clients'),

]