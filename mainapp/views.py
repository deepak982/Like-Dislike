from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login as auth_login,logout as auth_logout
from .models import *
import random
from .otp import phone_otp
from rest_framework import viewsets
from .serializers import *

def home(request):
    if request.user.username:
        image = Image.objects.all()
        history = History.objects.all()
        return render(request,"index.html",{'images':image,'username':request.user,'history':history})
    else:
        return redirect('/login/')


def history(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        action = request.POST.get('action')

        try:
            image = Image.objects.get(name=name)
        except Image.DoesNotExist:
            
            return JsonResponse({'success': False, 'error': 'Image not found'})
    
        history = History(user = request.user, image = image, action = action)
        history.save()

        return JsonResponse({'status': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def login (request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        try:
            profile = Profile.objects.get(mobile=phone)

            if otp == stored_otp:
                user = profile.user
                auth_login(request, user)  # Renamed the function to avoid conflict
                return redirect('/')
            else:
                return render(request,'login.html',{'message':"Invalid OTP"})
        except Profile.DoesNotExist:
            return render(request,'login.html',{'message': 'Phone number not found Please Create Account'})

    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = phone).first()


        if check_user or check_profile:
            return render(request,'signup.html',{'message':"User already exist",'class':'Danger'})


        user = User(username = username,email = email , first_name = name , password = repassword)
        Otp = request.session['otp']
        profile = Profile(user = user , mobile = phone , otp = Otp)

        otp = request.POST.get('otp')

        if otp == Otp and password == repassword:
            user.save()
            profile.save()
            return render(request, 'signup.html', {'message': "Account Create Successfully!"})
        else:    
            return render(request, 'signup.html', {'message': "OTP Invalid!"})

    return render(request,'signup.html')

def send_otp(request):
    if request.method == 'POST':
        Otp = str(random.randint(1000 , 9999))
        request.session['otp'] = Otp
        phone = request.POST['phone']
        phone_otp(phone,Otp)
        return JsonResponse({'status':'Success'})
    else:
        return JsonResponse({'status':'Failed'})
    
def logout(request):
    auth_logout(request)
    return redirect('login')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer