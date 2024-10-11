from django.utils import timesince, timezone
from rest_framework import serializers

from app import models


def BuildTime(created_at):
    today = timezone.now().date()
    if today == created_at.date():
        date = created_at.time().strftime("%I:%M %p")
    else:
        date = f"{created_at.date()} {created_at.time().strftime('%I:%M %p')}"
    return date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]