from django.utils import timesince, timezone
from rest_framework import serializers
from django.db.models import Avg, Count

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
           "name",
            "email",
           
        ]



class BookSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    def get_avg_rating(self, obj):
        return getattr(obj, 'avg_rating', 0) or 0

    def get_total_reviews(self, obj):
        return getattr(obj, 'total_reviews', obj.book_reviews.count())

    class Meta:
        model = models.Book
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=models.Book.objects.all())

    def validate(self, attrs):
        user = self.context['request'].user
        book = attrs.get('book')

        if models.Review.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this book."}
            )
        return attrs

    class Meta:
        model = models.Review
        exclude = ["user"]