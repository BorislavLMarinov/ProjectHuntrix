from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
import re

def validate_username_regex(value):
    if not re.match(r'^[A-Za-z0-9_]+$', value):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores.",
            code='invalid_username'
        )

class Adult(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text="Required. 3-50 characters. Letters, digits and _ only.",
        validators=[
            validators.MinLengthValidator(3),
            validate_username_regex
        ],
        error_messages={
            'unique': "Oops! This username is already taken by another Huntrix member."
        }
    )

    password = models.CharField(
        max_length=30,
        help_text="Password must be at least 8 characters.",
        validators=[validators.MinLengthValidator(8)]
    )

    email = models.EmailField(
        unique=True,
        error_messages={'unique': "A user with this email already exists."}
    )

    age = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(18)],
        help_text="You must be at least 18 years old to manage Huntrix games."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class Teacher(Adult):
    school_name = models.CharField(     #mayby optional later on
        max_length=100,
        blank=True,
        null=True,
        verbose_name="KPOP Academy"
    )

    @property
    def dashboard_url(self):
        return "teacher_dashboard" #ToDo


class Parent(Adult):
    relationship_to_kid = models.CharField(     #mayby optional later on
        max_length=50,
        choices=[
            ('parent', 'Parent'),
            ('guardian', 'Guardian'),
            ('sibling', 'Older Sibling')],
        default='parent'
    )

    @property
    def dashboard_url(self):
        return "stats_page"  #ToDo