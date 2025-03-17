from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtain(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        token['user'] = user.username
        return token
