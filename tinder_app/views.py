import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.generic import *
from django.shortcuts import reverse, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from .services import *
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect


class ProfilesListForToday(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'tinder_app/index.html', context = {})
        elif request.user.is_staff:
            return render(request, 'tinder_app/admin_index.html', context={})
        else:
            profile = Profile.objects.get(user=request.user)
            profiles = get_profiles(profile)
            check_reciprocites(profile)

            return render(request, 'tinder_app/index.html', context = {'profiles': profiles})

    def post(self, request):
        if 'unlike' in request.POST:
            print('Не нравится')
            profile = Profile.objects.get(user=request.user)
            profile_to = Profile.objects.get(nickname=request.POST.get('unlike'))
            UnLike.objects.create(user_from=profile, user_to=profile_to)
            profiles = get_profiles(profile)
            context = {'profiles': profiles}
            return HttpResponseRedirect('/')
        elif 'like' in request.POST:
            print('Нравится')
            profile = Profile.objects.get(user=request.user)
            profile_to = Profile.objects.get(nickname=request.POST.get('like'))
            if Like.objects.filter(user_from = profile_to, user_to = profile).exists():
                print("есть лайк")
                Like.objects.create(user_from=profile, user_to=profile_to)
                Reciprocity.objects.create(user_1=profile, user_2=profile_to)
                Chat.objects.create(member_1 = profile, member_2  = profile_to)
                print("чат создан!")

            else:
                Like.objects.create(user_from=profile, user_to=profile_to)
            profiles = get_profiles(profile)

            return HttpResponseRedirect('/')


class ProfileLikes(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        likes = Like.objects.filter(user_from = profile)
        context = {'likes': likes}
        return render(request, 'tinder_app/profile_likes.html', context)


class ProfileSympathy(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        likes = Like.objects.filter(user_to=profile)
        context = {'likes': likes}
        return render(request, 'tinder_app/profile_sympathy.html', context)

    def post(self, request):
        if 'sympathy' in request.POST:
            profile = Profile.objects.get(user = request.user)
            like = Like.objects.get(id = request.POST.get('sympathy'))
            # print(like.user_from)
            # Like.objects.create(user_from = profile, user_to = like.user_from)
            likes = Like.objects.filter(user_to=profile)
            Reciprocity.objects.create(user_1=profile, user_2=like.user_from)
            Chat.objects.create(member_1 = profile, member_2 = like.user_from)
            Like.objects.get(id = request.POST.get('sympathy')).delete()
            context = {'likes': likes}
            return render(request, 'tinder_app/profile_sympathy.html', context)


class ProfileReciprocites(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        reciprocites = Reciprocity.objects.filter(Q(user_1 = profile) | Q(user_2 = profile))
        context = {'reciprocites': reciprocites, 'profile': profile}
        return render(request, 'tinder_app/profile_reciprocites.html', context)


class ChatList(View):
    def get(self, request):
        profile = Profile.objects.get(user = request.user)
        chats = Chat.objects.filter(Q(member_1 = profile) | Q(member_2 = profile))
        receivers = Chat.objects.exclude(Q(member_1 = profile) | Q(member_2 = profile))
        check_chats(profile)

        context = {'chats': chats, 'receivers': receivers, 'profile': profile}
        return render(request, 'tinder_app/chat_list.html', context)



class ChatWithRec(View):
    def get(self, request, id):
        message_form = MessageForm()
        profile = Profile.objects.get(user = request.user)

        chat = Chat.objects.get(id = id)
        messages = chat.message.all()
        context = {'chat': chat, 'profile': profile, 'form': message_form, 'messages': messages}
        return render(request, 'tinder_app/chat.html', context)

    def post(self, request, id):
        message_form = MessageForm(request.POST)
        profile = Profile.objects.get(user=request.user)
        chat = Chat.objects.get(id = id)
        messages = chat.message.all()

        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.message = message_form.cleaned_data['message']
            new_message.chat = chat
            new_message.author = profile
            new_message.pub_date = timezone.now()
            new_message.is_reader = False
            new_message.save()
            message_form = MessageForm()
            context = {'chat': chat, 'profile': profile, 'form': message_form, 'messages': messages}
            return redirect(chat.get_absolute_url())

        context = {'chat': chat, 'profile': profile, 'form': message_form, 'messages': messages}
        return render(request, 'tinder_app/chat.html', context)


class DeleteMessage(View):
    def get(self, request, message_id):
        profile = Profile.objects.get(user=request.user)
        message_to_del = get_object_or_404(Message, id = message_id, author = profile)
        message_form = MessageForm()

        context = {'profile': profile, 'message': message_to_del}
        return render(request, 'tinder_app/message_delete.html', context)

    def post(self, request, message_id):
        message_to_del = Message.objects.get(id=message_id)
        chat = Chat.objects.get(message = message_to_del)

        message_to_del.delete()
        messages = chat.message.all()
        form = MessageForm()

        profile = Profile.objects.get(user = request.user)
        context = {'chat': chat, 'profile': profile, 'form': form, 'messages': messages}
        return redirect(chat.get_absolute_url())


class DeleteLike(View):
    def post(self, request, id):
        like = Like.objects.get(id = id)
        print(like)
        profile = Profile.objects.get(user=request.user)
        likes = Like.objects.filter(user_from=profile)
        like.delete()
        context = {'likes': likes}
        return HttpResponseRedirect('/')


class OwnProfile(View):
    def get(self, request):
        profile = Profile.objects.get(user = request.user)
        context = {'profile': profile}
        return render(request, 'auth/own_profile.html', context)


class ProfilesList(View):
    def get(self, request):
        profiles = Profile.objects.all()

        context = {'profiles': profiles}
        return render(request, 'tinder_app/profile_list.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'auth/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('index')
        return render(request, 'auth/login.html', context={'form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()

        cities = []
        with open('C:/Users/amate/python/tinder_project/tinder/tinder_app/templates/auth/by-cities.json', encoding='UTF-8') as file:
            data = json.load(file)
            for i in range(0, 6):

                for city in data[0]['regions'][i]['cities']:
                    cities.append(city['name'])

        context = {'form': register_form, 'city_list': cities}
        return render(request, 'auth/registration.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.username = register_form.cleaned_data['username']
            new_user.email = register_form.cleaned_data['email']
            new_user.first_name = register_form.cleaned_data['firstname']
            new_user.last_name = register_form.cleaned_data['lastname']
            new_user.save()
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            request.POST.getlist('services')
            Profile.objects.create(user = new_user, nickname = new_user.username,
                                   firstname = register_form.cleaned_data['firstname'],
                                   lastname = register_form.cleaned_data['lastname'],
                                   location = request.POST.getlist('cities')[0],
                                   type = register_form.cleaned_data['type'])
            user = authenticate(username=register_form.cleaned_data['username'],
                                password=register_form.cleaned_data['password'])
            login(request, user)
            return redirect('index')
        print(register_form.errors)
        context = {'form': register_form}
        return redirect('registration')