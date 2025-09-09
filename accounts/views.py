from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from django.contrib.auth.hashers import make_password

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Wrong method"}, status=405)

    try:
        # Decode JSON safely
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validation
        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        # Create user
        user = User(username=username, email=email, password=make_password(password))
        user.save()

        return JsonResponse({
            "message": "User has been created successfully",
            "status": True
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
