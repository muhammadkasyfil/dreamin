from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class DreamAnimation(models.Model):
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DreamSound(models.Model):
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Dialogue(models.Model):
    name = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=255)
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
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reflections'
    )
    dream = models.ForeignKey(
        Dream, 
        on_delete=models.CASCADE, 
        related_name='reflections'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reflection on {self.dream.title} by {self.user.username}"

class DreamSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Session by {self.user.username} at {self.start_time}"