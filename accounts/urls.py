from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("accounts/", views.UsersView.as_view()),    
    path("accounts/newest/<int:num>/", views.NewestUsersView.as_view()),    
    path('login/', ObtainAuthToken.as_view()),   
    path("accounts/<uuid:pk>/", views.UserDetailView.as_view()),  
    path("accounts/<uuid:pk>/management/", views.UserManagementView.as_view()), 
      

]