from django.urls import path
from . import views

urlpatterns = [


 
    path('login/', views.user_login, name='user_login'), 
    path('',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('admin_pro/', views.admin_page, name='admin_pro'),
    path('search/', views.search, name="search"),
    path('createuser/', views.create_user, name='create_user'),
    path('edituser/<pk>/', views.edit_user, name='edit_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('logout/', views.user_logout, name='logout'),


    


    
]
