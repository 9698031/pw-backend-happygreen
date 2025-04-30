from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import (
    UserProfile, Group, GroupMembership, Post, PostImage, Location, Comment,
    Badge, UserBadge, Challenge, UserChallenge, Quiz, QuizQuestion, QuizAnswer,
    Product, RecognizedObject
)
from .serializers import (
    UserSerializer, UserProfileSerializer, GroupSerializer, GroupDetailSerializer,
    PostSerializer, PostDetailSerializer, PostImageSerializer, LocationSerializer,
    CommentSerializer, BadgeSerializer, UserBadgeSerializer,
    ChallengeSerializer, ChallengeDetailSerializer, UserChallengeSerializer,
    QuizSerializer, QuizQuestionSerializer, QuizAnswerSerializer,
    ProductSerializer, RecognizedObjectSerializer,
    UserCreateSerializer, UserProfileCreateUpdateSerializer,
    GroupCreateUpdateSerializer, PostCreateUpdateSerializer, CommentCreateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create user profile
        UserProfile.objects.create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserProfileCreateUpdateSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GroupDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return GroupCreateUpdateSerializer
        return GroupSerializer

    @action(detail=False, methods=['get'])
    def my_groups(self, request):
        groups = Group.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        group = self.get_object()
        user = request.user

        if GroupMembership.objects.filter(user=user, group=group).exists():
            return Response({"detail": "User is already a member of this group."},
                            status=status.HTTP_400_BAD_REQUEST)

        GroupMembership.objects.create(user=user, group=group)
        return Response({"detail": "Successfully joined the group."},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        group = self.get_object()
        user = request.user

        membership = get_object_or_404(GroupMembership, user=user, group=group)

        # Check if user is the creator
        if group.creator == user:
            return Response({"detail": "Creator cannot leave the group."},
                            status=status.HTTP_400_BAD_REQUEST)

        membership.delete()
        return Response({"detail": "Successfully left the group."},
                        status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def by_group(self, request):
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response({"detail": "Group ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.filter(group_id=group_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        post = self.get_object()

        # Check if user is the author
        if post.author != request.user:
            return Response({"detail": "Only the author can add images to this post."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def by_post(self, request):
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response({"detail": "Post ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        comments = Comment.objects.filter(post_id=post_id, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_badges(self, request):
        badges = UserBadge.objects.filter(user=request.user)
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChallengeDetailSerializer
        return ChallengeSerializer

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        challenge = self.get_object()
        user = request.user

        if UserChallenge.objects.filter(user=user, challenge=challenge).exists():
            return Response({"detail": "User has already joined this challenge."},
                            status=status.HTTP_400_BAD_REQUEST)

        UserChallenge.objects.create(user=user, challenge=challenge)
        return Response({"detail": "Successfully joined the challenge."},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        challenge = self.get_object()
        user = request.user

        user_challenge = get_object_or_404(UserChallenge, user=user, challenge=challenge)

        if user_challenge.completed:
            return Response({"detail": "Challenge already completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        user_challenge.completed = True
        user_challenge.completed_at = timezone.now()
        user_challenge.save()

        # Update user's eco_score
        profile = user.profile
        profile.eco_score += challenge.points
        profile.save()

        # Award badge if challenge has one
        if challenge.badge:
            UserBadge.objects.get_or_create(user=user, badge=challenge.badge)

        return Response({"detail": "Challenge completed successfully."},
                        status=status.HTTP_200_OK)


class UserChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserChallenge.objects.all()
    serializer_class = UserChallengeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_challenges(self, request):
        user_challenges = UserChallenge.objects.filter(user=request.user)
        serializer = UserChallengeSerializer(user_challenges, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def by_barcode(self, request):
        barcode = request.query_params.get('barcode')
        if not barcode:
            return Response({"detail": "Barcode is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, barcode=barcode)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class RecognizedObjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecognizedObject.objects.all()
    serializer_class = RecognizedObjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category']

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.query_params.get('category')
        if not category:
            return Response({"detail": "Category is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        objects = RecognizedObject.objects.filter(category=category)
        serializer = RecognizedObjectSerializer(objects, many=True)
        return Response(serializer.data)