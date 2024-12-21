from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Dream, DreamAnimation, DreamSound, Dialogue, Reflection, Profile
from django.contrib.auth.views import LogoutView
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import os
from django.conf import settings
from .forms import SignupForm

# Landing Page View
def index(request):
    return render(request, 'index.html', {})

@login_required
def home_view(request):
    search_query = request.GET.get('search', '')
    
    try:
        user_dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
        all_dreams = Dream.objects.all().order_by('-created_at')
        
        # Check if Cloudinary is properly configured
        if settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'):
            animations = DreamAnimation.objects.filter(file__isnull=False)
            sounds = DreamSound.objects.filter(file__isnull=False)
            dialogues = Dialogue.objects.filter(file__isnull=False)
            
            if search_query:
                user_dreams = user_dreams.filter(title__icontains=search_query)
                all_dreams = all_dreams.filter(title__icontains=search_query)
                animations = animations.filter(name__icontains=search_query)
                sounds = sounds.filter(name__icontains=search_query)
                dialogues = dialogues.filter(name__icontains=search_query)
            else:
                animations = animations.order_by('?')
                sounds = sounds.order_by('?')
                dialogues = dialogues.order_by('?')
        else:
            messages.warning(request, "Media features are temporarily unavailable.")
            animations = []
            sounds = []
            dialogues = []
            
            if search_query:
                user_dreams = user_dreams.filter(title__icontains=search_query)
                all_dreams = all_dreams.filter(title__icontains=search_query)
                
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        user_dreams = []
        all_dreams = []
        animations = []
        sounds = []
        dialogues = []
    
    context = {
        'user_dreams': user_dreams,
        'all_dreams': all_dreams,
        'animations': animations[:3] if animations else [],
        'sounds': sounds[:3] if sounds else [],
        'dialogues': dialogues[:3] if dialogues else [],
        'latest_dream': Dream.objects.filter(user=request.user).order_by('-created_at').first(),
        'search_query': search_query,
    }
    
    return render(request, "home.html", context)

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "index.html")
            
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Create or get profile after successful login
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
            
            # Update profile after session is created
            if request.session.session_key:
                profile.last_session_key = request.session.session_key
                profile.session_start = timezone.now()
                profile.session_expiry = timezone.now() + timezone.timedelta(days=1)
                profile.login_count += 1
                profile.save()
            
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, "index.html")

@login_required
def create_dream_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if not title:
            messages.error(request, "Title is required.")
            return redirect('create_dream')
            
        try:
            dream = Dream.objects.create(
                user=request.user,
                title=title,
                description=description
            )
            
            # Handle single animation
            animation_id = request.POST.get('animation')
            if animation_id:
                try:
                    animation = DreamAnimation.objects.get(id=animation_id)
                    dream.animations.add(animation)
                except ObjectDoesNotExist:
                    messages.warning(request, "Selected animation not found.")
            
            # Similar try-except blocks for sound and dialogue
            sound_id = request.POST.get('sound')
            if sound_id:
                try:
                    sound = DreamSound.objects.get(id=sound_id)
                    dream.sounds.add(sound)
                except ObjectDoesNotExist:
                    messages.warning(request, "Selected sound not found.")
                    
            dialogue_id = request.POST.get('dialogue')
            if dialogue_id:
                try:
                    dialogue = Dialogue.objects.get(id=dialogue_id)
                    dream.dialogues.add(dialogue)
                except ObjectDoesNotExist:
                    messages.warning(request, "Selected dialogue not found.")
            
            messages.success(request, "Dream created successfully!")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, "An error occurred while creating your dream.")
            return redirect('create_dream')
    
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
    try:
        dream = get_object_or_404(Dream, id=dream_id, user=request.user)
        context = {
            'dream': dream,
            'animation': dream.animations.first(),
            'sound': dream.sounds.first(),
            'dialogue': dream.dialogues.first(),
        }
        return render(request, 'dreamplayback.html', context)
    except Http404:
        messages.error(request, "Dream not found.")
        return redirect('home')

@login_required
def dream_detail(request, dream_id):
    dream = Dream.objects.get(id=dream_id, user=request.user)
    reflections = Reflection.objects.filter(dream=dream)
    context = {
        'dream': dream,
        'reflections': reflections
    }
    return render(request, 'dream_detail.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
