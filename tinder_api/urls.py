from django.urls import path
from .views import *

urlpatterns = [
    path('profiles/', ProfileListApiView.as_view(), name='profiles'),
    path('likes/', LikeListApiView.as_view(), name='likes'),
    path('unlikes/', UnLikeListApiView.as_view(), name='unlikes'),
    path('reciprocities/', ReciprocityListApiView.as_view(), name='reciprocities'),
    path('chats/', ChatListApiView.as_view(), name='chats'),
]