from django.core.mail import send_mail
from rest_framework import viewsets, pagination, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from .serializers import PostWorkoutSerializer, PostContentSerializer, TagSerializer, ContactSerializer, \
    RegisterSerializer, UserSerializer, CommentSerializer
from .models import PostWorkout, PostContent, Comment
from rest_framework import permissions


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class PostWorkoutViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'title']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostWorkoutSerializer
    queryset = PostWorkout.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class PostContentViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'title']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostContentSerializer
    queryset = PostContent.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class TagDetailView(generics.ListAPIView):
    serializer_class = PostContentSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return PostContent.objects.filter(tag=tag)


class AsideView(generics.ListAPIView):
    queryset = PostContent.objects.all().order_by('-id')[:3]
    serializer_class = PostContentSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['yourgymnastic@gmail.com'])
            return Response({"success": "Sent"})


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args,  **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = PostContent.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)

