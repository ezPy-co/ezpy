from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from installer_config.models import EnvironmentProfile


@login_required()
def profile(request):
    user = request.user
    profiles = EnvironmentProfile.objects.filter(user=user).all()
    return render(request, 'profile.html', {
        'user': user,
        'profiles': profiles,
    })
