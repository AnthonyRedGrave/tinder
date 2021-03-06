from .models import *
from django.db.models import Q

def get_profiles(profile):
    if profile.type == 'Man':
        profiles = list(Profile.objects.filter(type='Woman'))
        likes = Like.objects.filter(user_from = profile)
        dislikes = UnLike.objects.filter(user_from = profile)
        reciprocites = Reciprocity.objects.filter(Q(user_1 = profile) | Q(user_2 = profile))

        for pr in likes:
            profiles.remove(pr.user_to)
        for dis in dislikes:
            profiles.remove(dis.user_to)
        for rep in reciprocites:
            if rep.user_2 == profile:

                if rep.user_1 in profiles:
                    profiles.remove(rep.user_1)
            elif rep.user_1 == profile:

                if rep.user_2 in profiles:
                    profiles.remove(rep.user_2)
        return profiles
    else:
        profiles = list(Profile.objects.filter(type='Man'))

        likes = Like.objects.filter(user_from=profile)
        dislikes = UnLike.objects.filter(user_from=profile)
        reciprocites = Reciprocity.objects.filter(Q(user_1=profile) | Q(user_2=profile))

        for pr in likes:
            profiles.remove(pr.user_to)
        for dis in dislikes:
            profiles.remove(dis.user_to)
        for rep in reciprocites:
            if rep.user_2 == profile:

                if rep.user_1 in profiles:
                    profiles.remove(rep.user_1)
            elif rep.user_1 == profile:

                if rep.user_2 in profiles:
                    profiles.remove(rep.user_2)

        return profiles




def check_reciprocites(profile):
    likes = Like.objects.filter(Q(user_from = profile)|Q(user_to = profile))
    arr = []
    arr_to_del = []
    for like_1 in likes:
        for like_2 in likes:
            if like_1.user_from == like_2.user_to and like_1.user_to == like_2.user_from:
                if like_1 not in arr and like_2 not in arr:
                    arr.append(like_1)
                    arr.append(like_2)
                    recs = Reciprocity.objects.filter(Q(user_1 = like_1.user_from, user_2 = like_2.user_from) | Q(user_1 = like_1.user_to, user_2 = like_2.user_to))
                    if recs.exists():
                        print(recs)
                        arr_to_del.append(like_1)
                        arr_to_del.append(like_2)

                    else:
                        print("если симпатия не была создана, он создается здесь")
                        Reciprocity.objects.create(user_1 = like_1.user_from, user_2 = like_2.user_from)


    if len(arr_to_del) > 0:
        print("нужно удалить")
        for like in arr_to_del:
            like.delete()


def check_chats(profile):
    recs = Reciprocity.objects.filter(Q(user_1 = profile)| Q(user_2 = profile))
    for rec in recs:
        chats = Chat.objects.filter(Q(member_1 = rec.user_1, member_2 = rec.user_2) | Q(member_1 = rec.user_2, member_2 = rec.user_1))
        if chats.exists():
            print(chats)
        else:
            print(rec.user_1)
            print(rec.user_2)
            Chat.objects.create(member_1 = rec.user_1, member_2 = rec.user_2)
            print("чат создан")