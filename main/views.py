from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Dream, DreamAnimation, DreamSound, Dialogue, Reflection

# Landing Page View
def index(request):
    return render(request, 'index.html', {})

def home_view(request):
    return render(request, "home.html", {})

# Signup Form
class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email'
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password'
    }))

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 != password2:
                messages.error(request, "Passwords do not match!")
                return redirect('signup')

            # Create the user with an email
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f"Welcome, {username}! Your account has been created.")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "index.html")

@login_required
def create_dream(request):
    if request.method == 'POST':
        dream = Dream.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description')
        )
        
        # Handle animations
        animation_ids = request.POST.getlist('animations')
        dream.animations.set(DreamAnimation.objects.filter(id__in=animation_ids))
        
        # Handle sounds
        sound_ids = request.POST.getlist('sounds')
        dream.sounds.set(DreamSound.objects.filter(id__in=sound_ids))
        
        # Handle dialogues
        dialogue_ids = request.POST.getlist('dialogues')
        dream.dialogues.set(Dialogue.objects.filter(id__in=dialogue_ids))
        
        return redirect('dream_detail', dream_id=dream.id)
    
    context = {
        'animations': DreamAnimation.objects.all(),
        'sounds': DreamSound.objects.all(),
        'dialogues': Dialogue.objects.all(),
    }
    return render(request, 'main/dreamcreation.html', context)

@login_required
def create_reflection(request, dream_id):
    if request.method == 'POST':
        dream = Dream.objects.get(id=dream_id)
        reflection = Reflection.objects.create(
            user=request.user,
            dream=dream,
            content=request.POST.get('reflection')
        )
        return redirect('dream_detail', dream_id=dream.id)
    
    return render(request, 'main/dreamjournal.html', {
        'dream': Dream.objects.get(id=dream_id)
    })
