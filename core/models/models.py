from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .base import BaseModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()


class Classroom(BaseModel):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(
        User, through="Membership", related_name="classroom_membership"
    )

    def __str__(self):
        return self.name


class Membership(BaseModel):
    PENDING = 1
    ACCEPTED = 2
    STATUS_CHOICES = ((PENDING, "Pending"), (ACCEPTED, "Accepted"))
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACCEPTED)
    is_teacher = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_membership", fields=["user", "classroom"]
            )
        ]

    def __str__(self):
        desc = f"{self.classroom}: {self.user}, {self.get_status_display()}"
        if self.is_teacher:
            desc += ", teacher"
        return desc


class Assignment(BaseModel):
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()

    def __str__(self):
        return f"Assignment: {self.text}"


class Submission(BaseModel):
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    file_url = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.assignment}: {self.user}"


class Comment(BaseModel):
    submission = models.ForeignKey(Submission, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.FloatField()
    text = models.TextField()

    def __str__(self):
        return f"{self.timestamp}: {self.text}"
