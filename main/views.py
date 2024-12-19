from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Dream, DreamAnimation, DreamSound, Dialogue, Reflection
from django.contrib.auth.views import LogoutView

# Landing Page View
def index(request):
    return render(request, 'index.html', {})

@login_required
def home_view(request):
    search_query = request.GET.get('search', '')
    
    user_dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
    all_dreams = Dream.objects.all().order_by('-created_at')
    animations = DreamAnimation.objects.all()
    sounds = DreamSound.objects.all()
    dialogues = Dialogue.objects.all()
    
    if search_query:
        user_dreams = user_dreams.filter(title__icontains=search_query)
        all_dreams = all_dreams.filter(title__icontains=search_query)
        animations = animations.filter(name__icontains=search_query)
        sounds = sounds.filter(name__icontains=search_query)
        dialogues = dialogues.filter(name__icontains=search_query)
    else:
        # Only randomize if not searching
        animations = animations.order_by('?')
        sounds = sounds.order_by('?')
        dialogues = dialogues.order_by('?')
    
    context = {
        'user_dreams': user_dreams,
        'all_dreams': all_dreams,
        'animations': animations[:3],
        'sounds': sounds[:3],
        'dialogues': dialogues[:3],
        'latest_dream': Dream.objects.filter(user=request.user).order_by('-created_at').first(),
        'search_query': search_query,
    }
    return render(request, "home.html", context)

# Signup Form
class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Enter your username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Enter your email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Confirm your password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "signup.html", {'form': form})
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Log user in
            login(request, user)
            messages.success(request, f"Welcome to Dreamin, {username}!")
            return redirect('home')
    else:
        form = SignupForm()
    
    return render(request, "signup.html", {'form': form})

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
def create_dream_view(request):
    if request.method == 'POST':
        dream = Dream.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description')
        )
        
        # Handle single animation
        animation_id = request.POST.get('animation')
        if animation_id:
            dream.animations.add(DreamAnimation.objects.get(id=animation_id))
        
        # Handle single sound
        sound_id = request.POST.get('sound')
        if sound_id:
            dream.sounds.add(DreamSound.objects.get(id=sound_id))
        
        # Handle single dialogue
        dialogue_id = request.POST.get('dialogue')
        if dialogue_id:
            dream.dialogues.add(Dialogue.objects.get(id=dialogue_id))
        
        return redirect('home')
    
    context = {
        'animations': DreamAnimation.objects.all(),
        'sounds': DreamSound.objects.all(),
        'dialogues': Dialogue.objects.all(),
    }
    return render(request, 'dreamcreation.html', context)

@login_required
def create_reflection(request, dream_id):
    dream = Dream.objects.get(id=dream_id, user=request.user)
    if request.method == 'POST':
        reflection = Reflection.objects.create(
            user=request.user,
            dream=dream,
            content=request.POST.get('reflection')
        )
        messages.success(request, 'Reflection added successfully!')
        return redirect('dream_detail', dream_id=dream.id)
    
    context = {
        'dream': dream,
        'reflections': Reflection.objects.filter(dream=dream)
    }
    return render(request, 'dreamjournal.html', context)

@login_required
def dreamjournal_view(request):
    user_dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'dreams': user_dreams,
    }
    return render(request, 'dreamjournal.html', context)

@login_required
def dreamplayback_view(request, dream_id):
    dream = Dream.objects.get(id=dream_id, user=request.user)
    context = {
        'dream': dream,
        'animation': dream.animations.first(),
        'sound': dream.sounds.first(),
        'dialogue': dream.dialogues.first(),
    }
    return render(request, 'dreamplayback.html', context)

@login_required
def dream_detail(request, dream_id):
    dream = Dream.objects.get(id=dream_id, user=request.user)
    reflections = Reflection.objects.filter(dream=dream)
    context = {
        'dream': dream,
        'reflections': reflections
    }
    return render(request, 'dream_detail.html', context)
