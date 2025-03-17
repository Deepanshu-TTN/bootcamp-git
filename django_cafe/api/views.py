from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from api.serializers import UserSerializer



@api_view(['POST'])
def create_user(request):
    if request.data.get('is_staff', False):
        if not request.user.is_authenticated:
            return Response({'error': "Must be logged in to create staff accounts"}, status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_staff:
            return Response({'error': "Only Super User can create staff accounts"}, status.HTTP_403_FORBIDDEN)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    