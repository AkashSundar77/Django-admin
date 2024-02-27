from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
    


srb = False

@never_cache
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect('home')  
        return render(request, 'signup.html')
    return redirect('home')
         
@never_cache
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
                if user.is_superuser:
                    return redirect('admin_pro') 
            else:
                messages.error(request, "Invalid credentials")
        return render(request, 'login.html')
    return redirect('home')
    
@never_cache
def admin_page(request):
    if request.user.is_superuser:
        print('admin_pro')
        details = User.objects.all().exclude(is_superuser=True)
        return render(request,'admin.html',{'details':details})  
    return redirect("user_login")

@never_cache
def edit_user(request, pk):

    user = User.objects.get(id=pk)
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')
        print(new_username,new_email)
        user.username = new_username
        user.email = new_email
        user.save()
        messages.success(request, "User updated successfully")
        return redirect('admin_pro') 
    return render(request, 'edituser.html', {'user': user})
@never_cache
def create_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "User created successfully")
                return redirect('admin_pro') 
                messages.error(request, "Username already exists")
        return render(request, 'createuser.html')
    return redirect('user_login')

@never_cache
def search(request):
    srb = True
    if request.method == "POST":
        q = request.POST.get('q')
        adminU = User.objects.filter(Q(username__istartswith=q)).order_by("-date_joined").exclude(username = "akashsundar")
        if len(adminU):
            return render(request,'admin.html',{"srb" : srb , "adminU" : adminU })
        else:
            messages.warning(request,"No results found!")
            print(messages)
        
    return redirect('admin_pro') 

@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout (request)    
        return redirect ("user_login")
    return redirect ("user_login")
    

@never_cache
def home(request):
    print(request.user,request)
    if request.user.is_superuser:
            return redirect('admin_pro') 
    if request.user.is_authenticated:
        messages.success(request, "you are logged in")
        return render(request, 'home.html',)
    return redirect('user_login')

@never_cache
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            user.delete()
        except User.DoesNotExist:
            pass 
    return redirect('admin_pro')  
    