from django.urls import path
from .views import (
 RootAPIView, 
 RegisterView, LoginView, ProfileView

) 

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

]