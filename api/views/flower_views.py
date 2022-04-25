from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from ..models.flower import Flower
from ..serializers import FlowerSerializer

class Flowers(generics.ListCreateAPIView):
    # permission_classes=(IsAuthenticated,)
    # serializer_class = FlowerSerializer
    def get(self, request):
        """Index request"""
        # Get all the flowers:
        # flowers = Flower.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        # flowers = Flower.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        # data = FlowerSerializer(flowers, many=True).data
        # return Response({ 'flowers': data })
        # basic request to front end json
        flowers = Flower.objects.all()
        data = FlowerSerializer(flowers, many=True).data
        return JsonResponse(data)
        
    def post(self, request):
        """Create flowers"""
        print(request.data)
        flower = FlowerSerializer(data=request.data)
        if flower.is_valid():
            flower.save()
            return JsonResponse(flower.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(flower.errors, status=status.HTTP_400_BAD_REQUEST)

class FlowerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the flower to show
        flower = get_object_or_404(Flower, pk=pk)
        # # Only want to show owned flowers?
        # if request.user != mango.owner:
        #     raise PermissionDenied('Unauthorized, you do not own this mango')

        # Run the data through the serializer so it's formatted
        data = FlowerSerializer(flower).data
        return JsonResponse({ 'flower': data })