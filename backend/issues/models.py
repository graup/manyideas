from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.timezone import now
from config.utils import notify_slack
from autoslug import AutoSlugField
from .fields import HeatIndexField


class SoftDeletableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_date__isnull=True)


class SoftDeletableModel(models.Model):
    deleted_date = models.DateTimeField(_('date deleted'), blank=True, null=True)

    objects = models.Manager()
    available_objects = SoftDeletableManager()

    def soft_delete(self):
        self.deleted_date = now()
        self.save()
        print("soft deleted object %s " % self)
    
    class Meta:
        abstract = True


class Category(models.Model):
    label = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='label', unique=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('slug',)
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Tag(models.Model):
    KIND_CHOICES = (
        (0, 'like'),
        (1, 'flag'),
    )

    # TODO this is mising created_date

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    kind = models.IntegerField(default=0, choices=KIND_CHOICES)
    value = models.IntegerField(default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.TextField(blank=True, null=True)

    def __str__(self):
        return '<%s> %ss <%s>' % (self.author, self.get_kind_display(), self.content_object)


def notify_flag(sender, instance, created, **kwargs):
    if not created or not instance.kind == 1:
        return
    url = reverse("admin:%s_%s_change" % (instance.content_type.app_label, instance.content_type.model), args=(instance.object_id,))
    notify_slack('*New flag!* %s' % instance, url)
post_save.connect(notify_flag, sender=Tag)

class Location(models.Model):
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=250)
    external_id = models.CharField(max_length=250, db_index=True)

    def __str__(self):
        return self.name

class Issue(SoftDeletableModel):
    "A user-generated issue"
    title = models.CharField(max_length=250)
    text = models.TextField()
    created_date = models.DateTimeField(_('date created'), auto_now_add=True)
    modified_date = models.DateTimeField(_('date modified'), auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    slug = AutoSlugField(populate_from='title', unique=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)

    heat = HeatIndexField(score_field='score', timestamp_field='created_date')

    tag_set = GenericRelation(Tag)

    def __str__(self):
        return self.title

    def get_comment_count(self):
        return self.comment_set.count()
    
    def get_like_count(self):
        return self.tag_set.filter(kind=0).count()

    def set_user_liked(self, user, liked):
        likes = self.tag_set.filter(kind=0, author=user).all()
        if liked and not likes:
            tag = Tag(content_object=self, author=user, kind=0)
            tag.save()
        if not liked and likes:
            self.tag_set.filter(kind=0, author=user).delete()
        self.user_liked = liked

    @property
    def score(self):
        return self.get_like_count()

    @property
    def comments(self):
        return self.comment_set.filter(deleted_date__isnull=True)

    def flag(self, user, reason):
        tag = Tag(content_object=self, author=user, kind=1, data=reason)
        tag.save()
        return tag

    class Meta:
        ordering = ('-heat',)
        verbose_name = _("issue")


class Comment(SoftDeletableModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(_('date created'), auto_now_add=True)
    text = models.TextField()

    tag_set = GenericRelation(Tag)

    def flag(self, user, reason):
        tag = Tag(content_object=self, author=user, kind=1, data=reason)
        tag.save()
        return tag

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("comment")

    def __str__(self):
        if self.deleted_date is not None:
            return '(deleted) %s' % self.text[:50]
        return self.text[:50]
