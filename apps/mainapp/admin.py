from django.contrib import admin
from .models import ContactMessage, BlogPost, BlogDetail

admin.site.register(BlogPost)
admin.site.register(BlogDetail)
admin.site.register(ContactMessage)

# Register your models here.
