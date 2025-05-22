from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from tweet.forms import UserRegistrationForm, UserLoginForm

def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                ['anonymousperson02102003@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "Your message has been sent!")
        except BadHeaderError:
            messages.error(request, "Invalid header found.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

    return render(request, 'contact.html')
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    return render(request,'registration/register.html',{'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def custom_404_view(request, exception):
    return render(request, 'not_found.html', status=404)