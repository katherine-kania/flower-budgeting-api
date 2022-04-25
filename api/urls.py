from django.urls import path
from .views.flower_views import Flowers, FlowerDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('flowers/', Flowers.as_view(), name='flowers'),
    path('flowers/<int:pk>/', FlowerDetail.as_view(), name='flower_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
