from django.contrib import admin
from .models import Profile, Dream, Reflection, DreamAnimation, DreamSound, DreamSession, Dialogue

admin.site.register(Profile)
admin.site.register(Dream)
admin.site.register(Reflection)
admin.site.register(DreamAnimation)
admin.site.register(DreamSound)
admin.site.register(DreamSession)
admin.site.register(Dialogue)