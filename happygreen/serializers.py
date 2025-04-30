from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Badge, UserBadge, Group, GroupMembership, Post, Comment,
    RecognizedObject, ScanRecord, Quiz, QuizQuestion, QuizOption,
    QuizAttempt, Challenge, ChallengeParticipation, Product, ProductScan
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'points', 'created_at']
        read_only_fields = ['points', 'created_at']


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon', 'points_required', 'created_at']
        read_only_fields = ['created_at']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge_details = BadgeSerializer(source='badge', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'username', 'badge_details', 'earned_at']
        read_only_fields = ['earned_at']


class GroupMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'username', 'role', 'joined_at']
        read_only_fields = ['joined_at']


class GroupSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'creator_username', 'members_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_members_count(self, obj):
        return obj.members.count()


class GroupDetailSerializer(GroupSerializer):
    members = GroupMembershipSerializer(source='groupmembership_set', many=True, read_only=True)

    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + ['members']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author_username', 'group_name', 'group',
            'image', 'latitude', 'longitude', 'location_name', 'comments_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.count()


class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['comments']


class RecognizedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognizedObject
        fields = [
            'id', 'name', 'description', 'category', 'eco_impact',
            'recycling_info', 'sustainability_score', 'image', 'created_at'
        ]
        read_only_fields = ['created_at']


class ScanRecordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    object_name = serializers.CharField(source='recognized_object.name', read_only=True)
    object_details = RecognizedObjectSerializer(source='recognized_object', read_only=True)

    class Meta:
        model = ScanRecord
        fields = [
            'id', 'username', 'object_name', 'object_details', 'image',
            'latitude', 'longitude', 'location_name', 'created_at'
        ]
        read_only_fields = ['created_at']


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ['id', 'text', 'is_correct']
        extra_kwargs = {
            'is_correct': {'write_only': True}  # Hide correct answer in response
        }


class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'options', 'created_at']
        read_only_fields = ['created_at']


class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'points', 'questions_count', 'created_at']
        read_only_fields = ['created_at']

    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(QuizSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ['questions']


class QuizAttemptSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'username', 'quiz_title', 'quiz', 'score',
            'completed', 'started_at', 'completed_at'
        ]
        read_only_fields = ['started_at', 'completed_at']


class ChallengeSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'points', 'participants_count',
            'start_date', 'end_date', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_participants_count(self, obj):
        return obj.participants.count()


class ChallengeParticipationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)

    class Meta:
        model = ChallengeParticipation
        fields = [
            'id', 'username', 'challenge_title', 'challenge',
            'completed', 'joined_at', 'completed_at'
        ]
        read_only_fields = ['joined_at', 'completed_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'barcode', 'name', 'description', 'manufacturer',
            'eco_friendly', 'recyclable', 'sustainability_score',
            'eco_info', 'alternatives', 'image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductScanSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = ProductScan
        fields = ['id', 'username', 'product_details', 'created_at']
        read_only_fields = ['created_at']