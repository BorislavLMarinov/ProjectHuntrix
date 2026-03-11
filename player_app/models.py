from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from core_common.models import Teacher, Parent
import re


def validate_stage_name(value):
    if not re.match(r'^[A-Za-z ]+$', value):
        raise ValidationError(
            "Stage names can only contain letters and spaces.",
            code='invalid_stage_name'
        )


class KidProfile(models.Model):
    creator = models.ForeignKey(
        'core_common.Parent',
        on_delete=models.CASCADE,
        related_name='kids',
        null=True, blank=True
    )

    teacher = models.ForeignKey(
        'core_common.Teacher',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='students'
    )

    name = models.CharField(
        max_length=50,
        validators=[validators.MinLengthValidator(2), validate_stage_name],
        help_text="Enter the kid's name or KPOP stage name."
    )

    total_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Kid Profile"
        ordering = ['-total_points']

    def __str__(self):
        return self.name

    def update_level(self):
        new_level = (self.total_points // 100) + 1
        if new_level != self.level:
            self.level = new_level
            self.save()


class Avatar(models.Model):
    STYLE_CHOICES = [
        ('vocal', 'Vocalist'),
        ('dance', 'Main Dancer'),
        ('rap', 'Lead Rapper'),
        ('visual', 'Visual/Center'),
    ]

    kid = models.ForeignKey(
        KidProfile,
        on_delete=models.CASCADE,
        related_name='avatars'
    )

    display_name = models.CharField(max_length=50)
    style = models.CharField(max_length=10, choices=STYLE_CHOICES, default='vocal')

    image = models.ImageField(
        upload_to='avatars/',
        null=True, blank=True,
        help_text="Upload a KPOP-styled character image."
    )

    bio = models.TextField(
        max_length=200,
        blank=True,
        help_text="Write a short debut introduction!"
    )

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.display_name} ({self.get_style_display()})"