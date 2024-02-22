from django.contrib import admin
from home.models import Directory, File, Chunk

admin.site.register(File)
admin.site.register(Directory)
admin.site.register(Chunk)