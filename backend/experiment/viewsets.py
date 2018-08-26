from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from experiment.treatments import auto_assign_user

from .serializers import *
from .models import ClassificationResult
from issues.serializers import UserSerializer


class ClassificationResultViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ClassificationResult.objects
    serializer_class = ClassificationResultSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        #serializer = ClassificationResultSerializer(serializer.instance)
        serializer = UserSerializer(serializer.instance.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        instance = serializer.save()
        auto_assign_user(instance.user)
