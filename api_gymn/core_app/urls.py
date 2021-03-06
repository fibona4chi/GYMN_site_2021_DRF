from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('workouts', PostWorkoutViewSet, basename='workouts')
router.register('posts', PostContentViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path("tags/", TagView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("aside/", AsideView.as_view()),
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path("comments/", AddCommentView.as_view()),
    path("comments/<slug:post_slug>/", GetCommentView.as_view()),
]
