from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import ExtUser
from django.contrib.auth import authenticate, login
from Registration.abstract_factory import MaterialFactory, BootstrapFactory
# Create your views here.
def signup(request):
    if request.method == "POST":
        if User.objects.filter(username = request.POST['username']).count() == 0:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(username = request.POST['username'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = request.POST['password1'])
                user.save()
                extuser = ExtUser(username = user, gender = request.POST['gender'], mobile = request.POST['mobile'], dob = request.POST['dob'])
                extuser.save()
                username = request.POST['username']
                password = request.POST['password1']
                user = authenticate(username = username, password = password)
                login(request,user)
                return redirect('Details:Skills')
            else:
                context={'error':"Password and Re-type Password doesn't match!"}
        else:
            context = {'error':"Username already exists!"}
    else:
        context = {}
    return render(request,'Registration/signup.html',context=context)

def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('Details:Feed', page=1)
        else:
            context = {'error':'Incorrect username or password!'}
    else:
        context = {}

    factory = BootstrapFactory()
    return render(request, factory.createLogin().getLogin(), context=context)

def intro(request):
    return render(request,'Registration/Intro.html')