from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .models import (
    Profile, Badge, UserBadge, Group, GroupMembership, Post, Comment,
    RecognizedObject, ScanRecord, Quiz, QuizQuestion, QuizOption,
    QuizAttempt, Challenge, ChallengeParticipation, Product, ProductScan
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, ProfileSerializer,
    BadgeSerializer, UserBadgeSerializer, GroupSerializer, GroupDetailSerializer,
    PostSerializer, PostDetailSerializer, CommentSerializer,
    RecognizedObjectSerializer, ScanRecordSerializer, QuizSerializer,
    QuizDetailSerializer, QuizAttemptSerializer, ChallengeSerializer,
    ChallengeParticipationSerializer, ProductSerializer, ProductScanSerializer, GroupMembershipSerializer
)
from .permissions import IsOwnerOrReadOnly, IsGroupMember, IsGroupAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def badges(self, request, pk=None):
        user = self.get_object()
        badges = UserBadge.objects.filter(user=user)
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        user = self.get_object()
        groups = Group.objects.filter(members=user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def scans(self, request, pk=None):
        user = self.get_object()
        scans = ScanRecord.objects.filter(user=user)
        serializer = ScanRecordSerializer(scans, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def product_scans(self, request, pk=None):
        user = self.get_object()
        product_scans = ProductScan.objects.filter(user=user)
        serializer = ProductScanSerializer(product_scans, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def award(self, request, pk=None):
        badge = self.get_object()
        user = request.user

        # Check if user already has this badge
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            return Response({"detail": "User already has this badge"}, status=status.HTTP_400_BAD_REQUEST)

        # Award the badge
        user_badge = UserBadge.objects.create(user=user, badge=badge)

        # Update user points
        profile = Profile.objects.get(user=user)
        profile.points += badge.points_required
        profile.save()

        serializer = UserBadgeSerializer(user_badge)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GroupDetailSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        group = serializer.save(creator=self.request.user)
        GroupMembership.objects.create(user=self.request.user, group=group, role='ADMIN')

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        group = self.get_object()
        user = request.user

        # Check if user is already a member
        if GroupMembership.objects.filter(user=user, group=group).exists():
            return Response({"detail": "User is already a member of this group"}, status=status.HTTP_400_BAD_REQUEST)

        # Add user to group
        GroupMembership.objects.create(user=user, group=group, role='MEMBER')

        return Response({"detail": "Successfully joined the group"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        group = self.get_object()
        user = request.user

        # Check if user is a member
        try:
            membership = GroupMembership.objects.get(user=user, group=group)
        except GroupMembership.DoesNotExist:
            return Response({"detail": "User is not a member of this group"}, status=status.HTTP_400_BAD_REQUEST)

        # If user is the creator of the group, they cannot leave
        if group.creator == user:
            return Response({"detail": "Creator cannot leave the group"}, status=status.HTTP_400_BAD_REQUEST)

        # Remove user from group
        membership.delete()

        return Response({"detail": "Successfully left the group"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        group = self.get_object()
        memberships = GroupMembership.objects.filter(group=group)
        serializer = GroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        group = self.get_object()
        posts = Post.objects.filter(group=group).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsGroupMember]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        user = request.user
        content = request.data.get('content')

        if not content:
            return Response({"detail": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            post=post,
            author=user,
            content=content
        )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecognizedObjectViewSet(viewsets.ModelViewSet):
    queryset = RecognizedObject.objects.all()
    serializer_class = RecognizedObjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category']

    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = RecognizedObject.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))


class ScanRecordViewSet(viewsets.ModelViewSet):
    queryset = ScanRecord.objects.all()
    serializer_class = ScanRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ScanRecord.objects.all()
        return ScanRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the scan record
        scan = serializer.save(user=self.request.user)

        # Update user points
        profile = Profile.objects.get(user=self.request.user)
        profile.points += 5  # Award 5 points for each scan
        profile.save()

        # Check if user qualifies for any badge
        self.check_for_badges(self.request.user)

        return scan

    def check_for_badges(self, user):
        # Get number of scans by user
        scans_count = ScanRecord.objects.filter(user=user).count()

        # Get badges the user doesn't have yet
        user_badges = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        available_badges = Badge.objects.exclude(id__in=user_badges)

        # Check if user qualifies for any badge based on points
        user_profile = Profile.objects.get(user=user)
        for badge in available_badges:
            if badge.points_required <= user_profile.points:
                UserBadge.objects.create(user=user, badge=badge)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        quiz = self.get_object()
        user = request.user

        # Check if user has an active attempt
        active_attempt = QuizAttempt.objects.filter(user=user, quiz=quiz, completed=False).first()
        if active_attempt:
            serializer = QuizAttemptSerializer(active_attempt)
            return Response(serializer.data)

        # Create new attempt
        attempt = QuizAttempt.objects.create(user=user, quiz=quiz)

        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        user = request.user
        answers = request.data.get('answers', [])  # Format: [{"question_id": 1, "option_id": 2}, ...]

        # Find active attempt
        try:
            attempt = QuizAttempt.objects.get(user=user, quiz=quiz, completed=False)
        except QuizAttempt.DoesNotExist:
            return Response({"detail": "No active quiz attempt found"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate score
        score = 0
        for answer in answers:
            question_id = answer.get('question_id')
            option_id = answer.get('option_id')

            try:
                option = QuizOption.objects.get(id=option_id, question_id=question_id)
                if option.is_correct:
                    score += 1
            except QuizOption.DoesNotExist:
                pass

        # Update attempt
        attempt.score = score
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()

        # Award points to user
        profile = Profile.objects.get(user=user)
        points_earned = (score / quiz.questions.count()) * quiz.points
        profile.points += int(points_earned)
        profile.save()

        # Check for badges
        self.check_for_badges(user)

        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data)

    def check_for_badges(self, user):
        # Similar to scan records badge check
        user_profile = Profile.objects.get(user=user)
        user_badges = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        available_badges = Badge.objects.exclude(id__in=user_badges)

        for badge in available_badges:
            if badge.points_required <= user_profile.points:
                UserBadge.objects.create(user=user, badge=badge)


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Challenge.objects.all()

        # Filter by active challenges
        active = self.request.query_params.get('active')
        if active and active.lower() == 'true':
            now = timezone.now()
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now)

        return queryset

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        challenge = self.get_object()
        user = request.user

        # Check if challenge is active
        now = timezone.now()
        if not (challenge.start_date <= now <= challenge.end_date):
            return Response({"detail": "Challenge is not active"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already joined
        if ChallengeParticipation.objects.filter(user=user, challenge=challenge).exists():
            return Response({"detail": "Already joined this challenge"}, status=status.HTTP_400_BAD_REQUEST)

        # Join challenge
        participation = ChallengeParticipation.objects.create(user=user, challenge=challenge)

        serializer = ChallengeParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        challenge = self.get_object()
        user = request.user

        # Check if user joined the challenge
        try:
            participation = ChallengeParticipation.objects.get(user=user, challenge=challenge)
        except ChallengeParticipation.DoesNotExist:
            return Response({"detail": "You have not joined this challenge"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already completed
        if participation.completed:
            return Response({"detail": "Challenge already completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Complete challenge
        participation.completed = True
        participation.completed_at = timezone.now()
        participation.save()

        # Award points
        profile = Profile.objects.get(user=user)
        profile.points += challenge.points
        profile.save()

        # Check for badges
        self.check_for_badges(user)

        serializer = ChallengeParticipationSerializer(participation)
        return Response(serializer.data)

    def check_for_badges(self, user):
        # Similar to other badge checks
        user_profile = Profile.objects.get(user=user)
        user_badges = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        available_badges = Badge.objects.exclude(id__in=user_badges)

        for badge in available_badges:
            if badge.points_required <= user_profile.points:
                UserBadge.objects.create(user=user, badge=badge)

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        challenge = self.get_object()
        participants = ChallengeParticipation.objects.filter(challenge=challenge)
        serializer = ChallengeParticipationSerializer(participants, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'barcode', 'manufacturer']

    @action(detail=False, methods=['get'])
    def by_barcode(self, request):
        barcode = request.query_params.get('barcode', None)
        if not barcode:
            return Response({"detail": "Barcode parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(barcode=barcode)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def scan(self, request, pk=None):
        product = self.get_object()
        user = request.user

        # Record the scan
        product_scan = ProductScan.objects.create(user=user, product=product)

        # Update user points
        profile = Profile.objects.get(user=user)
        profile.points += 2  # Award 2 points for scanning products
        profile.save()

        # Check for badges
        self.check_for_badges(user)

        serializer = ProductScanSerializer(product_scan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def check_for_badges(self, user):
        # Similar to other badge checks
        user_profile = Profile.objects.get(user=user)
        user_badges = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        available_badges = Badge.objects.exclude(id__in=user_badges)

        for badge in available_badges:
            if badge.points_required <= user_profile.points:
                UserBadge.objects.create(user=user, badge=badge)