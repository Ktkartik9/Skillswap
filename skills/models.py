from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class UserSkill(models.Model):

    TEACH = "teach"
    LEARN = "learn"

    SKILL_TYPE_CHOICES = [
        (TEACH, "Teach"),
        (LEARN, "Learn"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="user_skills"
    )

    skill_type = models.CharField(
        max_length=10,
        choices=SKILL_TYPE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "skill", "skill_type"],
                name="unique_user_skill_type"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.skill.name} - {self.skill_type}"