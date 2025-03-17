from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from authAPI.serializers import MyTokenObtain

class MyTokenObtainView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtain

