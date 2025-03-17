from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.contrib.auth.models import User
from usersAPI.serializers import  UserSerializer


class UsersList(ListAPIView):
    # for oauth
    # permission_classes = [IsAuthenticated, IsAdminUser, TokenHasReadWriteScope]

    #for session
    permission_classes = [IsAuthenticated, IsAdminUser,]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
