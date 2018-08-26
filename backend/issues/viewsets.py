from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.timezone import now
from .serializers import *
from .models import Issue
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime, timedelta
import pytz

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000

class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects
    serializer_class = CommentSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        if self.request.user != instance.author and not self.request.user.is_superuser: 
            raise PermissionDenied()
        instance.soft_delete()
    
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated,])
    def flag(self, request, **kwargs):
        self.kwargs = kwargs
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated()

        obj = self.get_object()
        obj.flag(self.request.user, self.request.data['reason'])
        context = {
            'request': request
        }
        serializer = CommentSerializer(obj, context=context)
        return Response(serializer.data)

class IssueViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Issue.available_objects
    serializer_class = IssueSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = LargeResultsSetPagination
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = self.queryset
        if self.request.method == "POST":
            return qs
        # Add like count
        qs = qs.annotate(like_count=Count('tag_set', filter=Q(tag_set__kind=0), distinct=True))
        # Add comment count
        qs = qs.annotate(comment_count=Count('comment', filter=Q(comment__deleted_date__isnull=True), distinct=True))
        # Add if user has liked this issue
        if self.request.user and self.request.user.is_authenticated:
            qs = qs.annotate(
                user_liked=Count('tag_set', filter=Q(tag_set__kind=0) & Q(tag_set__author=self.request.user), distinct=True),
                user_commented=Count('comment', filter=Q(comment__deleted_date__isnull=True) & Q(comment__author=self.request.user), distinct=True)
            )
        return qs
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.like_count = 0
        instance.comment_count = 0

    def perform_destroy(self, instance):
        if self.request.user != instance.author and not self.request.user.is_superuser: 
            raise PermissionDenied()
        instance.soft_delete()
    
    @list_route(permission_classes=[IsAuthenticated,], url_name='stats', methods=['get'])
    def stats(self, request, pk=None):
        tz = pytz.timezone('Asia/Seoul')
        today_local = now().astimezone(tz).date()
        today_local_time = tz.localize(datetime(today_local.year, today_local.month, today_local.day))
        filter_today = Q(created_date__gt=today_local_time.astimezone(pytz.utc)) & Q(created_date__lt=now())
        filter_week = Q(created_date__gt=today_local_time.astimezone(pytz.utc) - timedelta(days=6)) & Q(created_date__lt=now())
        filter_today_i = Q(issue__created_date__gt=today_local_time.astimezone(pytz.utc)) & Q(issue__created_date__lt=now())
        filter_week_i = Q(issue__created_date__gt=today_local_time.astimezone(pytz.utc) - timedelta(days=6)) & Q(issue__created_date__lt=now())
        filter_today_c = Q(comment__created_date__gt=today_local_time.astimezone(pytz.utc)) & Q(comment__created_date__lt=now())
        filter_week_c = Q(comment__created_date__gt=today_local_time.astimezone(pytz.utc) - timedelta(days=6)) & Q(comment__created_date__lt=now())
        data = {
            'number_of_issues': {
                'today': Issue.available_objects.filter(filter_today).count(),
                'week': Issue.available_objects.filter(filter_week).count()
            },
            'number_of_comments': {
                'today': Comment.available_objects.filter(filter_today).count(),
                'week': Comment.available_objects.filter(filter_week).count()
            },
            'number_of_contrbutors': {
                'today': User.objects.annotate(
                    count_issues=Count('issue__id', filter=filter_today_i),
                    count_comments=Count('comment__id', filter=filter_today_c)
                ).filter(Q(count_issues__gt=0) | Q(count_comments__gt=0)).count(),
                'week': User.objects.annotate(
                    count_issues=Count('issue__id', filter=filter_week_i),
                    count_comments=Count('comment__id', filter=filter_week_c)
                ).filter(Q(count_issues__gt=0) | Q(count_comments__gt=0)).count()
            }
        }
        return Response(data)

    @detail_route(permission_classes=[IsAuthenticatedOrReadOnly,], url_name='comments')
    def comments(self, request, **kwargs):
        """Show non-deleted comments for this issue"""
        self.kwargs = kwargs
        #if not self.request.user or not self.request.user.is_authenticated:
        #    raise NotAuthenticated()

        obj = self.get_object()
        context = {
            'request': request
        }
        qs = obj.comment_set.filter(deleted_date__isnull=True)
        serializer = CommentSerializer(qs, many=True, context=context)
        return Response(serializer.data)
    
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated,])
    def like(self, request, **kwargs):
        self.kwargs = kwargs
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated()

        obj = self.get_object()
        obj.set_user_liked(self.request.user, self.request.data['liked'])
        obj.like_count = obj.tag_set.filter(kind=0).count()
        obj.comment_count = obj.comment_set.filter(deleted_date__isnull=True).count()
        context = {
            'request': request
        }
        serializer = IssueSerializer(obj, context=context)
        return Response(serializer.data)
    
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated,])
    def flag(self, request, **kwargs):
        self.kwargs = kwargs
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated()

        obj = self.get_object()
        obj.flag(self.request.user, self.request.data['reason'])
        obj.like_count = obj.tag_set.filter(kind=0).count()
        obj.comment_count = obj.comment_set.filter(deleted_date__isnull=True).count()
        context = {
            'request': request
        }
        serializer = IssueSerializer(obj, context=context)
        return Response(serializer.data)


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route()
    def me(self, request, pk=None):
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated()

        obj = User.objects.get(pk=request.user.id)
        context = {
            'request': request
        }
        serializer = UserSerializer(obj, context=context)
        return Response(serializer.data)
    
    @list_route(url_path='me/updates', methods=['get'])
    def me_updates(self, request, pk=None):
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated()

        since_ts = int(request.query_params['since'])
        since_dt = datetime.utcfromtimestamp(since_ts/1000.0).replace(tzinfo=pytz.utc)
        
        # Find issues with new comments
        issues = Issue.available_objects.filter(
            author=self.request.user,
            comment__created_date__gte=since_dt,
            comment__deleted_date__isnull=True
        ).exclude(
            comment__author=self.request.user
        )

        context = {
            'request': request
        }
        serializer = IssueSerializer(issues, many=True, context=context)
        return Response(serializer.data)
