from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='create_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.DetailView.as_view()),
    path('api/logout/<int:pk>/', views.LogoutView.as_view(), name='create_token'),

]
