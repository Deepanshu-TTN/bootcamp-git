# from django.urls import path
# from usersAPI import views
from rest_framework.routers import DefaultRouter
from usersAPI.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

# urlpatterns = [
#     path('all/', views.UsersList.as_view(), name='fetch_users'),
#     path('<pk>/', views.UserDetails.as_view(), name='user_datail')
# ]
