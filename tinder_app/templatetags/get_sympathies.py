from django import template
from ..models import *

register = template.Library()

@register.filter
def get_sympathy_count(user):
    if user.is_staff:
        return 0
    else:
        profile = Profile.objects.get(user = user)

        likes = Like.objects.filter(user_to = profile)
        return len(likes)

