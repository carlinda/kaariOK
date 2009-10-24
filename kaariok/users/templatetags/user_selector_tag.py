from django import template

from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('users/templatetags/user_selector.html')
def user_selector(token):
    users = User.objects.all().extra(select={'username_upper': 'upper(username)'}).order_by('username_upper')
    return {'users':users, 'selected_user':token}