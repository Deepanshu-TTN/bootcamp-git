from django.urls import path, include
from rest_framework.routers import DefaultRouter
from oauth2_provider.views import TokenView, RevokeTokenView
from api import views

router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewset)

urlpatterns = [
    #auth stuff
    path('auth/register/', views.create_user, name='register'),
    path('auth/token/', TokenView.as_view(), name='token'),
    path('auth/token-revoke/', RevokeTokenView.as_view(), name='token-revoke'),
    
    path('users/', views.UserList.as_view(), name='users-list'),
    path('users/<str:pk>/', views.UserDetail.as_view(), name='users-list'),
    
    #public apis
    
    #management apis
    path('', include(router.urls))
    
    
    #customer apis
    
    
]
