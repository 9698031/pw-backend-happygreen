from django.contrib import admin
from .models import (
    Profile, Badge, UserBadge, Group, GroupMembership, Post, Comment,
    RecognizedObject, ScanRecord, Quiz, QuizQuestion, QuizOption,
    QuizAttempt, Challenge, ChallengeParticipation, Product, ProductScan
)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'created_at')
    search_fields = ('user__username', 'user__email')

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'created_at')
    search_fields = ('name',)

class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    search_fields = ('user__username', 'badge__name')

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at')
    search_fields = ('name', 'description', 'creator__username')
    inlines = [GroupMembershipInline]

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'group', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'group__name')
    inlines = [CommentInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')

class RecognizedObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sustainability_score', 'created_at')
    search_fields = ('name', 'description', 'category')
    list_filter = ('category', 'sustainability_score')

class ScanRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'recognized_object', 'created_at')
    search_fields = ('user__username', 'recognized_object__name', 'location_name')
    list_filter = ('recognized_object__category',)

class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 3

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')
    search_fields = ('question', 'quiz__title')
    inlines = [QuizOptionInline]

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuizQuestionInline]

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed', 'started_at', 'completed_at')
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('completed',)

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'start_date', 'end_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')

class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'completed', 'joined_at', 'completed_at')
    search_fields = ('user__username', 'challenge__title')
    list_filter = ('completed',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'manufacturer', 'eco_friendly', 'recyclable', 'sustainability_score')
    search_fields = ('name', 'description', 'barcode', 'manufacturer')
    list_filter = ('eco_friendly', 'recyclable', 'sustainability_score')

class ProductScanAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name', 'product__barcode')

# Registrazione dei modelli
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(RecognizedObject, RecognizedObjectAdmin)
admin.site.register(ScanRecord, ScanRecordAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeParticipation, ChallengeParticipationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductScan, ProductScanAdmin)