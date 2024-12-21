from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Profile, Dream, Reflection, DreamAnimation, DreamSound, DreamSession, Dialogue

class MediaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not all(settings.CLOUDINARY_STORAGE.values()):
            raise ValidationError("Cloudinary storage is not properly configured. Please contact the administrator.")
        super().save_model(request, obj, form, change)

admin.site.register(Profile)
admin.site.register(Dream)
admin.site.register(Reflection)
admin.site.register(DreamAnimation, MediaAdmin)
admin.site.register(DreamSound, MediaAdmin)
admin.site.register(DreamSession)
admin.site.register(Dialogue, MediaAdmin)