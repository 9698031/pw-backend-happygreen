from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Group, GroupMembership, Post, PostImage, Location, Comment,
    Badge, UserBadge, Challenge, UserChallenge, Quiz, QuizQuestion, QuizAnswer,
    Product, RecognizedObject
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', 'profile_picture', 'date_joined', 'eco_score')


class GroupMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ('id', 'user', 'joined_at', 'is_admin')


class GroupSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'created_at', 'creator',
                  'group_picture', 'members_count')

    def get_members_count(self, obj):
        return obj.members.count()


class GroupDetailSerializer(GroupSerializer):
    members = GroupMembershipSerializer(source='groupmembership_set', many=True, read_only=True)

    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + ('members',)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude', 'address', 'name')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'ml_tags', 'uploaded_at')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'parent', 'replies')

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'group', 'created_at',
                  'updated_at', 'post_type', 'likes_count', 'comments_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class PostDetailSerializer(PostSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ('images', 'location', 'comments')


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'icon', 'points')


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ('id', 'user', 'badge', 'earned_at')


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ('id', 'answer_text', 'is_correct')


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ('id', 'question_text', 'order', 'answers')


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'questions')


class ChallengeSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    badge = BadgeSerializer(read_only=True)
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'description', 'challenge_type', 'points',
                  'created_at', 'expires_at', 'creator', 'group', 'badge',
                  'participants_count')

    def get_participants_count(self, obj):
        return obj.participants.count()


class ChallengeDetailSerializer(ChallengeSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta(ChallengeSerializer.Meta):
        fields = ChallengeSerializer.Meta.fields + ('quiz',)


class UserChallengeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = UserChallenge
        fields = ('id', 'user', 'challenge', 'completed', 'completed_at')


class ProductSerializer(serializers.ModelSerializer):
    alternatives = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'barcode', 'name', 'description', 'sustainability_score',
                  'is_recyclable', 'eco_information', 'alternatives')

    def get_alternatives(self, obj):
        return ProductSerializer(obj.alternative_products.all(), many=True, context=self.context).data


class RecognizedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognizedObject
        fields = ('id', 'name', 'category', 'description', 'recycle_info', 'environmental_impact')


# Serializers for creating and updating objects
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture')


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'description', 'group_picture')

    def create(self, validated_data):
        user = self.context['request'].user
        group = Group.objects.create(creator=user, **validated_data)
        GroupMembership.objects.create(user=user, group=group, is_admin=True)
        return group


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'post_type', 'group', 'location')

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        user = self.context['request'].user
        post = Post.objects.create(author=user, **validated_data)

        if location_data:
            Location.objects.create(post=post, **location_data)

        return post

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if location_data:
            location, created = Location.objects.get_or_create(post=instance)
            for attr, value in location_data.items():
                setattr(location, attr, value)
            location.save()

        return instance


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'content', 'parent')

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(author=user, **validated_data)