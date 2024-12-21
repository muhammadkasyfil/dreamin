import os
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_session_key = models.CharField(max_length=100, blank=True, null=True)
    session_start = models.DateTimeField(null=True, blank=True)
    session_expiry = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB limit
        raise ValidationError("The maximum file size that can be uploaded is 10MB")

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.mp3', '.wav', '.ogg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class DreamAnimation(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='animations',
        validators=[validate_file_size, validate_file_extension],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        if self.file:
            return self.file.url if hasattr(self.file, 'url') else ''
        return ''

    def __str__(self):
        return self.name

class DreamSound(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='sounds',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        if self.file:
            return self.file.url if hasattr(self.file, 'url') else ''
        return ''

    def __str__(self):
        return self.name

class Dialogue(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='dialogues', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        if self.file:
            return self.file.url if hasattr(self.file, 'url') else ''
        return ''

    def __str__(self):
        return self.name

class Dream(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='dreams',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    animations = models.ManyToManyField(DreamAnimation, blank=True)
    sounds = models.ManyToManyField(DreamSound, blank=True)
    dialogues = models.ManyToManyField(Dialogue, blank=True)
    preview_video = models.FileField(upload_to='dream_previews/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.user.username if self.user else 'unknown'}"

class Reflection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='reflections')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reflection on {self.dream.title} by {self.user.username}"

class DreamSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session for {self.dream.title if self.dream else 'Unknown Dream'}"

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        username = cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
            
        return cleaned_data

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()