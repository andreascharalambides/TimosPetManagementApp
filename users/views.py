from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, UserLoginForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import PushSubscription


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class UserLoginView(LoginView):
    authentication_form = UserLoginForm


@csrf_exempt
@login_required
def save_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subscription = data.get('subscription', {})
        endpoint = subscription.get('endpoint')
        keys = subscription.get('keys', {})
        p256dh = keys.get('p256dh')
        auth = keys.get('auth')

        PushSubscription.objects.update_or_create(
            user=request.user,
            endpoint=endpoint,
            defaults={
                'p256dh': p256dh,
                'auth': auth
            }
        )

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
