import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserActionLog


@csrf_exempt
@login_required
def log_action(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        UserActionLog.objects.create(
            user=request.user,
            action=action,
        )

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
