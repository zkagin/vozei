from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Assignment, Classroom, Comment, Membership, Submission, User


class BaseModelAdmin(admin.ModelAdmin):
    exclude = ("created", "modified")


def inline_model(linked_model):
    class BaseModelInline(admin.TabularInline):
        model = linked_model
        exclude = ("created", "modified")
        extra = 2

    return BaseModelInline


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    def teaching(self, obj):
        return [m.classroom for m in obj.membership_set.filter(is_teacher=True).all()]

    def attending(self, obj):
        return [m.classroom for m in obj.membership_set.filter(is_teacher=False).all()]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "teaching", "attending")
    search_fields = ("email",)
    ordering = ("email",)
    exclude = ("username",)
    inlines = [inline_model(Membership)]


@admin.register(Classroom)
class ClassroomAdmin(BaseModelAdmin):
    def teachers(self, obj):
        return [m.user for m in obj.membership_set.filter(is_teacher=True).all()]

    def member_count(self, obj):
        return obj.members.count()

    def assignment_count(self, obj):
        return obj.assignment_set.count()

    list_display = (
        "name",
        "teachers",
        "member_count",
        "assignment_count",
        "created",
        "modified",
    )
    inlines = [inline_model(Assignment), inline_model(Membership)]


@admin.register(Assignment)
class AssignmentAdmin(BaseModelAdmin):
    def submission_count(self, obj):
        return obj.submission_set.count()

    list_display = (
        "text",
        "classroom",
        "user",
        "submission_count",
        "created",
        "modified",
    )
    ordering = ("created",)
    exclude = ("created", "modified")
    inlines = [inline_model(Submission)]


@admin.register(Submission)
class SubmissionAdmin(BaseModelAdmin):
    list_display = ("assignment", "user", "file_url")
    inlines = [inline_model(Comment)]


@admin.register(Comment)
class CommentAdmin(BaseModelAdmin):
    list_display = ("submission", "user", "timestamp", "text")


@admin.register(Membership)
class MembershipAdmin(BaseModelAdmin):
    list_display = ("classroom", "user", "status", "is_teacher")
