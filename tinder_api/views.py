from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    RetrieveAPIView, RetrieveDestroyAPIView
from django.contrib.auth.models import User
from .serializers import *
from tinder_app.models import *
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import *
from rest_framework.views import APIView


class Logout(APIView):

    def get(self, request, format = None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# Profile API====================================
class ProfileListApiView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user = self.request.user)


class ProfileCreateApiView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("create")
        print(request.data)
        serializer = CreateProfileSerializer(data=request.data)
        if serializer.is_valid():
            print('valid')
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class ProfileRetrieveApiView(RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileUpdateApiView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [IsAuthenticated]


# Like API====================================
class LikeListApiView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Like.objects.all()
        else:
            return Like.objects.filter(Q(user_from__nickname = self.request.user) | Q(user_to__nickname = self.request.user))


class LikeCreateApiView(ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Like.objects.all()
        else:
            return Like.objects.filter(Q(user_from__nickname = self.request.user) | Q(user_to__nickname = self.request.user))

    def create(self, request, *args, **kwargs):
            print("create")
            print(request.data)
            serializer = LikeSerializer(data = request.data)
            if serializer.is_valid():
                print('valid')
                serializer.create(validated_data=request.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)


class LikeRetrieveApiView(RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


# UnLike API====================================
class UnLikeListApiView(ListAPIView):
    queryset = UnLike.objects.all()
    serializer_class = UnLikeSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return UnLike.objects.all()
        else:
            return UnLike.objects.filter(Q(user_from__nickname = self.request.user) | Q(user_to__nickname = self.request.user))


class UnLikeCreateApiView(ListCreateAPIView):
    queryset = UnLike.objects.all()
    serializer_class = UnLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UnLike.objects.all()
        else:
            return UnLike.objects.filter(Q(user_from__nickname = self.request.user) | Q(user_to__nickname = self.request.user))

    def create(self, request, *args, **kwargs):
        print("create")
        print(request.data)
        serializer = UnLikeSerializer(data=request.data)
        if serializer.is_valid():
            print('valid')
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UnLikeRetrieveApiView(RetrieveDestroyAPIView):
    queryset = UnLike.objects.all()
    serializer_class = UnLikeSerializer
    permission_classes = [IsAuthenticated]


# Reciprocity API====================================
class ReciprocityListApiView(ListAPIView):
    queryset = Reciprocity.objects.all()
    serializer_class = ReciprocitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reciprocity.objects.all()
        else:
            return Reciprocity.objects.filter(Q(user_1__nickname = self.request.user) | Q(user_2__nickname = self.request.user))


class ReciprocityRetrieveApiView(RetrieveDestroyAPIView):
    queryset = Reciprocity.objects.all()
    serializer_class = ReciprocitySerializer
    permission_classes = [IsAuthenticated]


# Chat API====================================
class ChatListApiView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Chat.objects.all()
        else:
            return Chat.objects.filter(Q(member_1__nickname = self.request.user) | Q(member_2__nickname = self.request.user))


# Message API====================================
class MessageListApiView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        else:
            return Message.objects.filter(author__nickname = self.request.user)