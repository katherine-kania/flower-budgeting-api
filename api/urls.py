from django.urls import path
from .views.flower_views import Flowers, FlowerDetail
from .views.order_views import Orders, OrderDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('flowers/', Flowers.as_view(), name='flowers'),
    path('flowers/<int:pk>/', FlowerDetail.as_view(), name='flower_detail'),
    path('flowers/create/', Flowers.as_view(), name='flowers_create'),
    path('flowers/<int:pk>/delete/', FlowerDetail.as_view(), name='flower_delete'),
    path('orders/', Orders.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('orders/create/', Orders.as_view(), name='orders_create'),
    path('orders/<int:pk>/delete/', OrderDetail.as_view(), name='order_delete'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-pw')
]
