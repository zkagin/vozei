from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Classroom, Assignment


class BaseModelAdmin(admin.ModelAdmin):
    exclude = ("created", "modified")


class BaseModelInline(admin.TabularInline):
    exclude = ("created", "modified")
    extra = 3


class ClassroomInline(BaseModelInline):
    model = Classroom


class AssignmentInline(BaseModelInline):
    model = Assignment
    fk_name = "classroom"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    def ownership_count(self, obj):
        return obj.classroom_set.count()

    def membership_count(self, obj):
        return obj.classroom_membership.count()

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
    list_display = (
        "email",
        "ownership_count",
        "membership_count",
        "first_name",
        "last_name",
    )
    search_fields = ("email",)
    ordering = ("email",)
    exclude = ("username",)
    inlines = [ClassroomInline]


@admin.register(Classroom)
class ClassroomAdmin(BaseModelAdmin):
    def member_count(self, obj):
        return obj.members.count()

    def assignment_count(self, obj):
        return obj.assignment_set.count()

    list_display = (
        "name",
        "owner",
        "member_count",
        "assignment_count",
        "created",
        "modified",
    )
    inlines = [AssignmentInline]
    exclude = ("created", "modified")


@admin.register(Assignment)
class AssignmentAdmin(BaseModelAdmin):
    list_display = ("title", "classroom", "created", "modified")
    ordering = ("created",)
    exclude = ("created", "modified")
