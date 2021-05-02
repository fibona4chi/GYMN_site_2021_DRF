from django.contrib import admin
from .models import PostWorkout, PostContent, Comment


class PostWorkoutAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(PostWorkout, PostWorkoutAdmin)
admin.site.register(PostContent, PostContentAdmin)
admin.site.register(Comment, CommentAdmin)