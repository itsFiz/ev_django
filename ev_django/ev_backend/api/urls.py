from . import views
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('auth/register/', views.resident_register),
    path('auth/logout/', views.resident_logout),
    path('auth/user/' , views.get_user),
    path('auth/logoutall/', views.resident_logout_all),
    path('auth/login/', views.resident_login),    
    path('verify/', views.admin_verify),
    path('residents/', views.get_residents),
    path('deleteuser/', views.admin_delete),
    



]
