from django.db import models
from django.contrib.auth.models import User
from django import forms

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class DreamAnimation(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='animations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DreamSound(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='sounds/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Dialogue(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='dialogues/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
        return cleaned_data