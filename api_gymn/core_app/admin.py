from django.contrib import admin
from .models import *


class PostWorkoutAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(PostWorkout, PostWorkoutAdmin)
admin.site.register(PostContent, PostContentAdmin)