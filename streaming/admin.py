from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Comment)