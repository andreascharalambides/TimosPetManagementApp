from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, UserLoginForm
import json
from django.http import JsonResponse, HttpResponse
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
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            print("Received data:", data)  # Debugging log

            # Extract subscription details directly from the root JSON object
            endpoint = data.get('endpoint')
            keys = data.get('keys', {})
            p256dh = keys.get('p256dh')
            auth = keys.get('auth')

            # Validate required fields
            if not endpoint or not p256dh or not auth:
                print("Incomplete subscription data.")  # Debugging log
                return JsonResponse({'error': 'Incomplete subscription data.'}, status=400)

            # Save or update the subscription
            PushSubscription.objects.update_or_create(
                user=request.user,
                endpoint=endpoint,
                defaults={
                    'p256dh': p256dh,
                    'auth': auth
                }
            )

            # Return success response
            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            print("Invalid JSON data.")  # Debugging log
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            print(f"Error saving subscription: {e}")  # Debugging log
            return JsonResponse({'error': 'An error occurred while saving the subscription.'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def service_worker(request):
    service_worker_content = """
    self.addEventListener('push', function(event) {
        const data = event.data.json();
        console.log('Push notification received:', data);

        const options = {
            body: data.body,
            icon: '/static/icons/notification-icon.png',
        };

        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    });
    """
    return HttpResponse(service_worker_content, content_type='application/javascript')
