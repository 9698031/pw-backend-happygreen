from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'badges', views.BadgeViewSet)
router.register(r'user-badges', views.UserBadgeViewSet)
router.register(r'challenges', views.ChallengeViewSet)
router.register(r'user-challenges', views.UserChallengeViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'objects', views.RecognizedObjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]