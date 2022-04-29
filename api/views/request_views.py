from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.request import Request as RequestModel
from ..serializers import RequestSerializer

# Create your views here.
class Requests(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = RequestSerializer
    def get(self, request):
        """Index request"""
        # Get all the requests:
        # requests = Request.objects.all()
        # Filter the requests by owner, so you can only see your owned requests
        requests = RequestModel.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = RequestSerializer(requests, many=True).data
        return Response({ 'requests': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['owner'] = request.user.id
        # Serialize/create request
        request = RequestSerializer(data=request.data)
        # If the request data is valid according to our serializer...
        if request.is_valid():
            # Save the created request & send a response
            request.save()
            return Response({ 'request': request.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(request.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the request to show
        Request = get_object_or_404(RequestModel, pk=pk)
        # Only want to show owned requests?
        if request.user != request.owner:
            raise PermissionDenied('Unauthorized, you do not own this request')

        # Run the data through the serializer so it's formatted
        data = RequestSerializer(request).data
        return Response({ 'request': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate requests to delete
        request = get_object_or_404(RequestModel, pk=pk)
        # Check the request's owner against the user making this request
        if request.user != request.owner:
            raise PermissionDenied('Unauthorized, you do not own this Request')
        # Only delete if the user owns the request
        request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate request
        # get_object_or_404 returns a object representation of our request
        request = get_object_or_404(RequestModel, pk=pk)
        # Check the request's owner against the user making this request
        if request.user != request.owner:
            raise PermissionDenied('Unauthorized, you do not own this request')

        # Ensure the owner field is set to the current user's ID
        request.data['owner'] = request.user.id
        # Validate updates with serializer
        data = RequestSerializer(request, data=request.data, partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)