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

@login_required
def home_view(request):
    search_query = request.GET.get('search', '')
    
    user_dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
    all_dreams = Dream.objects.all().order_by('-created_at')
    
    if search_query:
        user_dreams = user_dreams.filter(title__icontains=search_query)
        all_dreams = all_dreams.filter(title__icontains=search_query)
    
    context = {
        'user_dreams': user_dreams,
        'all_dreams': all_dreams,
        'random_animations': DreamAnimation.objects.order_by('?')[:3],
        'random_sounds': DreamSound.objects.order_by('?')[:3],
        'random_dialogues': Dialogue.objects.order_by('?')[:3],
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
        
        # Handle animations
        animation_ids = request.POST.getlist('animations')
        dream.animations.set(DreamAnimation.objects.filter(id__in=animation_ids))
        
        # Handle sounds
        sound_ids = request.POST.getlist('sounds')
        dream.sounds.set(DreamSound.objects.filter(id__in=sound_ids))
        
        # Handle dialogues
        dialogue_ids = request.POST.getlist('dialogues')
        dream.dialogues.set(Dialogue.objects.filter(id__in=dialogue_ids))
        
        return redirect('home')
    
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

@login_required
def dreamjournal_view(request):
    user_dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'dreams': user_dreams,
    }
    return render(request, 'dreamjournal.html', context)

@login_required
def dreamplayback_view(request):
    return render(request, 'dreamplayback.html')

@login_required
def dream_detail(request, dream_id):
    dream = Dream.objects.get(id=dream_id, user=request.user)
    reflections = Reflection.objects.filter(dream=dream)
    context = {
        'dream': dream,
        'reflections': reflections
    }
    return render(request, 'dream_detail.html', context)
