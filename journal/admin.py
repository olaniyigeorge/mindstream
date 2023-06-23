from django.contrib import admin

from .models import Entry, Tag
# Register your models here.


admin.site.register(Entry)
admin.site.register(Tag)
