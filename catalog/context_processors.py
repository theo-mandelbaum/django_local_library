from django.contrib.auth.models import AnonymousUser

def can_mark_returned(request):
    if isinstance(request.user, AnonymousUser):
        return {'can_mark_returned': False}
    return {'can_mark_returned': request.user.has_perm('catalog.can_mark_returned')}