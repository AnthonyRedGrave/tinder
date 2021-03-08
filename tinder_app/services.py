from .models import *
from django.db.models import Q
import json
from math import *


def get_profiles(profile):
        type = profile.type
        profiles = list(Profile.objects.exclude(type=type))
        likes = Like.objects.filter(user_from=profile)
        dislikes = UnLike.objects.filter(user_from=profile)
        reciprocites = Reciprocity.objects.filter(Q(user_1=profile) | Q(user_2=profile))
        print(dislikes)

        for pr in likes:
            profiles.remove(pr.user_to)
        for dis in dislikes:
            print(dis.user_to)
            profiles.remove(dis.user_to)
        for rep in reciprocites:
            if rep.user_2 == profile:
                if rep.user_1 in profiles:
                    profiles.remove(rep.user_1)
            elif rep.user_1 == profile:

                if rep.user_2 in profiles:
                    profiles.remove(rep.user_2)
        return profiles
    # else:
    #     profiles = list(Profile.objects.filter(type='Man'))
    #
    #     likes = Like.objects.filter(user_from=profile)
    #     dislikes = UnLike.objects.filter(user_from=profile)
    #     reciprocites = Reciprocity.objects.filter(Q(user_1=profile) | Q(user_2=profile))
    #
    #     for pr in likes:
    #         profiles.remove(pr.user_to)
    #     for dis in dislikes:
    #         profiles.remove(dis.user_to)
    #     for rep in reciprocites:
    #         if rep.user_2 == profile:
    #             if rep.user_1 in profiles:
    #                 profiles.remove(rep.user_1)
    #         elif rep.user_1 == profile:
    #
    #             if rep.user_2 in profiles:
    #                 profiles.remove(rep.user_2)
    #
    #     return profiles


def check_reciprocites(profile):
    likes = Like.objects.filter(Q(user_from=profile) | Q(user_to=profile))
    arr = []
    arr_to_del = []
    for like_1 in likes:
        for like_2 in likes:
            if like_1.user_from == like_2.user_to and like_1.user_to == like_2.user_from:
                if like_1 not in arr and like_2 not in arr:
                    arr.append(like_1)
                    arr.append(like_2)
                    recs = Reciprocity.objects.filter(
                        Q(user_1=like_1.user_from, user_2=like_2.user_from) | Q(user_1=like_1.user_to,
                                                                                user_2=like_2.user_to))
                    if recs.exists():
                        print(recs)
                        arr_to_del.append(like_1)
                        arr_to_del.append(like_2)

                    else:
                        print("если симпатия не была создана, он создается здесь")
                        Reciprocity.objects.create(user_1=like_1.user_from, user_2=like_2.user_from)

    if len(arr_to_del) > 0:
        print("нужно удалить")
        for like in arr_to_del:
            like.delete()


def check_chats(profile):
    recs = Reciprocity.objects.filter(Q(user_1=profile) | Q(user_2=profile))
    for rec in recs:
        chats = Chat.objects.filter(
            Q(member_1=rec.user_1, member_2=rec.user_2) | Q(member_1=rec.user_2, member_2=rec.user_1))
        if chats.exists():
            print(chats)
        else:
            print(rec.user_1)
            print(rec.user_2)
            Chat.objects.create(member_1=rec.user_1, member_2=rec.user_2)
            print("чат создан")


def calcDist(lat_A, long_A, lat_B, long_B):
    distance = (sin(radians(lat_A)) *
                sin(radians(lat_B)) +
                cos(radians(lat_A)) *
                cos(radians(lat_B)) *
                cos(radians(long_A - long_B)))
    distance = (degrees(acos(distance))) * 69.09
    return distance

def is_near_distance(type):
    if type == '1':
        return 10
    elif type == '2':
        return 25
    elif type == '3':
        return 1500

def count_of_swipes(type):
    if type == '1':
        return 20
    elif type == '2':
        return 100
    elif type == '3':
        return 1500



def get_near_profiles(profile):
    profiles = get_profiles(profile) # все профили, противоположного пола
    near_profiles = []

    profile_city = profile.location
    sub_type = profile.sub_type
    near_dist = is_near_distance(sub_type)
    cities_and_distance = {}
    with open('C:/Users/amate/python/tinder_project/tinder/tinder_app/templates/auth/by-cities.json',
              encoding='UTF-8') as file:
        data = json.load(file)
        for i in range(0, 6):
            for town in data[0]['regions'][i]['cities']:
                if profile_city == town['name']:
                    lat_A = town['lat']
                    long_A = town['lng']

        for profile in profiles:
            for i in range(0, 6):
                for town in data[0]['regions'][i]['cities']:
                    if profile.location == town['name']:
                        lat_B = town['lat']
                        long_B = town['lng']
                        distance = int(calcDist(lat_A, long_A, lat_B, long_B)) * 2
                        if distance <= near_dist:
                            near_profiles.append(profile)
                            cities_and_distance[profile.location] = distance

    return (cities_and_distance, near_profiles)
