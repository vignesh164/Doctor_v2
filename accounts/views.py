from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import custom_permission
from accounts.models import User


class GetUser(APIView):
    permission_classes = [custom_permission.IsDoctor,]

    def get(self, request):
        return Response(
            data={"data": list(User.objects.filter(groups__name__in=['Patient']).values('username', 'id'))},
            status=status.HTTP_200_OK
        )
