from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.flower import Flower
from ..serializers import FlowerSerializer

class Flowers(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = FlowerSerializer
    def get(self, request):
        """Index request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        flowers = Flower.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = FlowerSerializer(flowers, many=True).data
        return Response({ 'flowers': data })
