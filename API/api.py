from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from .serializers import *


class UserAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(token.key)


class LeadListApi(APIView):

    def get(self, request):
        model = Lead.objects.all()
        serializer = LeadSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class LeadDetailApi(APIView):
    def get(self, request, id):
        try:
            model = Lead.objects.get(id=id)
        except Lead.DoesNotExist:
            return Response("User does not exists",status = status.HTTP_404_NOT_FOUND)
        serializer = LeadSerializer(model)
        return Response(serializer.data)

    def delete(self,request, id):
        model = Lead.objects.get(id = id)
        model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        model = Lead.objects.get(id=id)
        serializer = LeadSerializer(model,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
