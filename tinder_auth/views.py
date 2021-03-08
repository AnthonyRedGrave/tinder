from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import json
from .forms import RegisterInfoForm
from django.views.generic import *
from django.contrib.auth import authenticate, login
from tinder_app.forms import *
from tinder_app.services import *
from django.shortcuts import redirect


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'tinder_auth/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('index')
        return render(request, 'tinder_auth/login.html', context={'form': login_form})


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
        return render(request, 'tinder_auth/registration.html', context)

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
            return redirect('registration-2')
        print(register_form.errors)
        context = {'form': register_form}
        return redirect('registration')


class RegisterInfoView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user = request.user)
        form = RegisterInfoForm(instance=profile)

        return render(request, 'tinder_auth/registration-2.html', context={'profile': profile, 'form': form})

    def post(self, request):
        profile = Profile.objects.get(user = request.user)
        form = RegisterInfoForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            profile.main_photo = form.cleaned_data['main_photo']
            profile.description = form.cleaned_data['description']
            profile.sub_type = form.cleaned_data['sub_type']
            profile.main_photo = form.cleaned_data['main_photo']
            profile.save()
            print(profile.description)
            return redirect('index')
        return render(request, 'tinder_auth/registration-2.html', context={'profile': profile, 'form': form})