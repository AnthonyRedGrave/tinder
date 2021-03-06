from rest_framework import serializers
from tinder_app.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user_from = ProfileSerializer()
    user_to = ProfileSerializer()

    class Meta:
        model = Like
        fields = '__all__'


class UnLikeSerializer(serializers.ModelSerializer):
    user_from = ProfileSerializer()
    user_to = ProfileSerializer()

    class Meta:
        model = UnLike
        fields = '__all__'


class ReciprocitySerializer(serializers.ModelSerializer):
    user_1 = ProfileSerializer()
    user_2 = ProfileSerializer()

    class Meta:
        model = Reciprocity
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    member_1 = ProfileSerializer()
    member_2 = ProfileSerializer()

    class Meta:
        model = Chat
        fields = '__all__'