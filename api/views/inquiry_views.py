from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.inquiry import Inquiry as InquiryModel
from ..serializers import InquirySerializer

# Create your views here.
class Inquirys(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = InquirySerializer
    def get(self, request):
        """Index request"""
        # Get all the inquirys:
        # inquirys = inquiry.objects.all()
        # Filter the inquirys by owner, so you can only see your owned inquirys
        inquirys = InquiryModel.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = InquirySerializer(inquirys, many=True).data
        return Response({ 'inquirys': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['owner'] = request.user.id
        # Serialize/create inquiry
        inquiry = InquirySerializer(data=request.data)
        # If the inquiry data is valid according to our serializer...
        if inquiry.is_valid():
            # Save the created inquiry & send a response
            inquiry.save()
            return Response({ 'inquiry': inquiry.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(inquiry.errors, status=status.HTTP_400_BAD_REQUEST)

class InquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the inquiry to show
        inquiry = get_object_or_404(InquiryModel, pk=pk)
        # Only want to show owned inquirys?
        if request.user != inquiry.owner:
            raise PermissionDenied('Unauthorized, you do not own this inquiry')

        # Run the data through the serializer so it's formatted
        data = InquirySerializer(inquiry).data
        return Response({ 'inquiry': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate inquiry to delete
        inquiry = get_object_or_404(InquiryModel, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != inquiry.owner:
            raise PermissionDenied('Unauthorized, you do not own this inquiry')
        # Only delete if the user owns the inquiry
        inquiry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate inquiry
        # get_object_or_404 returns a object representation of our inquiry
        inquiry = get_object_or_404(InquiryModel, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != inquiry.owner:
            raise PermissionDenied('Unauthorized, you do not own this inquiry')

        # Ensure the owner field is set to the current user's ID
        request.data['owner'] = request.user.id
        # Validate updates with serializer
        data = InquirySerializer(inquiry, data=request.data, partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)