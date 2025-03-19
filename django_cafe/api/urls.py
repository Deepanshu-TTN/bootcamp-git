from django.urls import path, include
from oauth2_provider.views import TokenView, RevokeTokenView
from api import views


urlpatterns = [
    #auth stuff
    path('auth/register/', views.create_user, name='register'),
    path('auth/token/', TokenView.as_view(), name='token'),
    path('auth/token-revoke/', RevokeTokenView.as_view(), name='token-revoke'),
    
    #public apis
    
    #management apis
    
    #customer apis
    
    
]
