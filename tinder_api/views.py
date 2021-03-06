from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .serializers import *
from tinder_app.models import *


class ProfileListApiView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class LikeListApiView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class UnLikeListApiView(ListAPIView):
    queryset = UnLike.objects.all()
    serializer_class = UnLikeSerializer


class ReciprocityListApiView(ListAPIView):
    queryset = Reciprocity.objects.all()
    serializer_class = ReciprocitySerializer


class ChatListApiView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer