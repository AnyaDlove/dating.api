from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Photo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="photos/")
    is_main = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_main", "-uploaded_at"]

    def __str__(self):
        return f"Фото {self.user} (главное: {self.is_main})"

    def save(self, *args, **kwargs):
        if self.is_main:
            Photo.objects.filter(user=self.user, is_main=True).exclude(
                pk=self.pk
            ).update(is_main=False)
        super().save(*args, **kwargs)


@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


class Like(models.Model):
    LIKE_CHOICES = [
        ("like", "Лайк"),
        ("dislike", "Дизлайк"),
    ]
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_given",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_received",
    )
    kind = models.CharField(max_length=10, choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.kind}"


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="views_made",
    )
    viewed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="views_received",
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.viewer} смотрел {self.viewed}"


class Invitation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принято"),
        ("declined", "Отклонено"),
    ]
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invitations_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invitations_received",
    )
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Приглашение от {self.from_user} к {self.to_user}"
