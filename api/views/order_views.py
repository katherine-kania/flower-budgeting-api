from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from ..models.order import Order
from ..serializers import OrderSerializer

# Create your views here.
class Orders(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = OrderSerializer
    def get(self, request):
        """Index request"""
        # Get all the orders:
        # orders = Order.objects.all()
        # Filter the orders by owner, so you can only see your owned orders
        orders = Order.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = OrderSerializer(orders, many=True).data
        return JsonResponse({ 'orders': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['order']['owner'] = request.user.id
        # Serialize/create order
        order = OrderSerializer(data=request.data['order'])
        # If the order data is valid according to our serializer...
        if order.is_valid():
            # Save the created order & send a response
            order.save()
            return JsonResponse({ 'order': order.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return JsonResponse(order.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the order to show
        order = get_object_or_404(Order, pk=pk)
        # Only want to show owned orders?
        if request.user != order.owner:
            raise PermissionDenied('Unauthorized, you do not own this order')

        # Run the data through the serializer so it's formatted
        data = OrderSerializer(order).data
        return JsonResponse({ 'order': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate order to delete
        order = get_object_or_404(Order, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != order.owner:
            raise PermissionDenied('Unauthorized, you do not own this order')
        # Only delete if the user owns the order
        order.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Order
        # get_object_or_404 returns a object representation of our Order
        order = get_object_or_404(Order, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != order.owner:
            raise PermissionDenied('Unauthorized, you do not own this order')

        # Ensure the owner field is set to the current user's ID
        request.data['order']['owner'] = request.user.id
        # Validate updates with serializer
        data = OrderSerializer(order, data=request.data['order'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return JsonResponse(data.errors, status=status.HTTP_400_BAD_REQUEST)
