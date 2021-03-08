from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-view'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh-view'),

    path('profiles/', ProfileListApiView.as_view(), name='api-profiles'),
    path('profiles/create/', ProfileCreateApiView.as_view(), name='api-profiles-create'),
    path('profiles/<int:pk>/', ProfileRetrieveApiView.as_view(), name='api-profiles-retrieve'),
    path('profiles/<int:pk>/update/', ProfileUpdateApiView.as_view(), name='api-profiles-update'),

    path('likes/', LikeListApiView.as_view(), name='api-likes'),
    path('likes/create/', LikeCreateApiView.as_view(), name='api-likes-create'),
    path('likes/<int:pk>/', LikeRetrieveApiView.as_view(), name = 'api-likes-retrieve'),

    path('unlikes/', UnLikeListApiView.as_view(), name='api-unlikes'),
    path('unlikes/create/', UnLikeCreateApiView.as_view(), name = 'api-unlikes-create'),
    path('unlikes/<int:pk>/', UnLikeRetrieveApiView.as_view(), name = 'api-unlikes-retrieve'),

    path('reciprocities/', ReciprocityListApiView.as_view(), name='api-reciprocities'),
    path('reciprocities/<int:pk>/', ReciprocityRetrieveApiView.as_view(), name = 'api-reciprocities-retrieve'),


    path('chats/', ChatListApiView.as_view(), name='api-chats'),

    path('messages/', MessageListApiView.as_view(), name='api-messages'),
]