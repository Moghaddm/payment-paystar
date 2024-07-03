# from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = BasicAuthentication
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self):
        return Response('hi')
