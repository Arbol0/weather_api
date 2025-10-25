from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

class Controller(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

