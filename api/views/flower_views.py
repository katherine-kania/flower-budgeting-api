from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.flower import Flower
from ..serializers import FlowerSerializer

class Flowers(generics.ListCreateAPIView):
    # permission_classes=(IsAuthenticated,)
    # serializer_class = FlowerSerializer
    def get(self, request):
        """Index request"""
        # Get all the flowers:
        # flowers = Flower.objects.all()
        # Filter the flowers by owner, so you can only see your owned mangos
        # flowers = Flower.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        # data = FlowerSerializer(flowers, many=True).data
        # return Response({ 'flowers': data })
        # basic request to front end json
        flowers = Flower.objects.all()
        data = FlowerSerializer(flowers, many=True).data
        return Response({'flowers': data})
        # return Response(data)
        
    def post(self, request):
        """Create flowers"""
        print(request.data)
        flower = FlowerSerializer(data=request.data)
        if flower.is_valid():
            flower.save()
            return Response(flower.data, status=status.HTTP_201_CREATED)
        else:
            return Response(flower.errors, status=status.HTTP_400_BAD_REQUEST)

class FlowerDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the flower to show
        flower = get_object_or_404(Flower, pk=pk)
        # # Only want to show owned flowers?
        # if request.user != flower.owner:
        #     raise PermissionDenied('Unauthorized, you do not own this flower')

        # Run the data through the serializer so it's formatted
        data = FlowerSerializer(flower).data
        return Response({ 'flower': data })
    

    def delete(self, request, pk):
        """Delete request"""
        # Locate flower to delete
        flower = get_object_or_404(Flower, pk=pk)
        # Check the flower's owner against the user making this request
        # if request.user != flower.owner:
        #     raise PermissionDenied('Unauthorized, you do not own this flower')
        # Only delete if the user owns the flower
        flower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Flower
        # get_object_or_404 returns a object representation of our Flower
        flower = get_object_or_404(Flower, pk=pk)
        # Check the flower's owner against the user making this request
        # if request.user != flower.owner:
        #     raise PermissionDenied('Unauthorized, you do not own this flower')

        # Ensure the owner field is set to the current user's ID
        request.data['owner'] = request.user.id
        # Validate updates with serializer
        data = FlowerSerializer(flower, data=request.data, partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
