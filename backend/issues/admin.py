from django.contrib import admin
from django.db.models.functions import Now
from django.urls import reverse
from django.utils.safestring import mark_safe 
from .models import Category, Issue, Comment, Tag, Location

admin.site.register(Category, admin.ModelAdmin)

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('author', 'kind_display', 'content_link', 'data',)
    read_only_fields = ('content_link', 'kind_display',)
    list_filter = ('kind', 'content_type',)

    def content_link(self, obj):
        content_type = obj.content_type
        if not content_type:
            return ''
        return mark_safe('<a href="{}">{}: {}</a>'.format(
            reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(obj.content_object.pk,)),
            content_type.model.title(), obj.content_object
        ))
    content_link.short_description = 'content object'

    def kind_display(self, obj):
        color = 'inherit'
        if obj.kind == 1:
            color = 'red'
        return mark_safe('<span style="color: {}">{}</span>'.format(
            color,
            obj.get_kind_display()
        ))
    kind_display.short_description = 'kind'
admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('issue', 'author', 'text', 'created_date', 'deleted_date',)
    actions = ['soft_delete']

    def soft_delete(self, request, queryset):
        rows_updated = queryset.update(deleted_date=Now())
        self.message_user(request, "%d comments successfully soft-deleted." % rows_updated)
    soft_delete.short_description = "Soft-delete comment"

admin.site.register(Comment, CommentAdmin)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class IssueAdmin(admin.ModelAdmin):
    model = Issue
    list_display = ('title', 'created_date', 'deleted_date', 'author', 'score', 'heat',)
    inlines = [
        CommentInline,
    ]
    actions = ['recalc_heat', 'soft_delete']

    def soft_delete(self, request, queryset):
        rows_updated = queryset.update(deleted_date=Now())
        self.message_user(request, "%d issues successfully soft-deleted." % rows_updated)
    soft_delete.short_description = "Soft-delete issue"

    def recalc_heat(self, request, queryset):
        rows_updated = 0
        for issue in queryset.all():
            issue.save()
            rows_updated += 1
        self.message_user(request, "%d issues successfully updated." % rows_updated)
    recalc_heat.short_description = "Re-calculate heat"
admin.site.register(Issue, IssueAdmin)
admin.site.register(Location, admin.ModelAdmin)
