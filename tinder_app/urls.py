from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', ProfilesListForToday.as_view(), name = 'index'),
    path('profile/', OwnProfile.as_view(), name = 'own_profile'),
    path('your_likes/', ProfileLikes.as_view(), name = 'your_likes'),
    path('likes/', ProfileSympathy.as_view(), name = 'likes'),
    path('delete_like/<int:id>', DeleteLike.as_view(), name='delete_like'),

    path('reciprocites/', ProfileReciprocites.as_view(), name = 'reciprocites'),
    path('chats/', ChatList.as_view(), name='chats'),
    path('chat/<int:id>/', ChatWithRec.as_view(), name='chat'),
    path('chat/<int:message_id>/delete/', DeleteMessage.as_view(), name = 'delete_message'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = '/'), name = 'logout'),

    path('profiles/', ProfilesList.as_view(), name='profiles-list'),
]