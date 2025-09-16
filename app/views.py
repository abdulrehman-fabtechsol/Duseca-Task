from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg , Count

from app import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    serializers = serializers.UserSerializer
    queryset = models.User.objects.all()
    http_method_names = ["get"]

    @action(detail=False, methods=["get"])
    def top_active_user_reviewed(self, request, *args, **kwargs):
        top_user = (models.Review.objects.values("user").annotate(review_count=Count("id")).order_by("-review_count").first())
        user = models.User.objects.get(id=top_user["user"])

        user_data = serializers.UserSerializer(user, context=self.get_serializer_context()).data

        return Response({
            "most_active_user": user_data,
            "review_count": top_user["review_count"],
        })

    @action(detail=False, methods=["get"])
    def top_5_active_user_reviewed(self, request, *args, **kwargs):
        top_5_users = models.User.objects.annotate(review_count=Count("user_reviews")).filter(review_count__gt=5).order_by("-review_count")[:5]
        return Response(serializers.UserSerializer(top_5_users, many=True, context=self.get_serializer_context()).data)


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()
    
    @action(detail=True, methods=["get"])
    def highest_rating(self, request, *args, **kwargs):
        books_filterted = (models.Book.objects.annotate(avg_rating=Avg("book_reviews__rating")).order_by("-avg_rating")[:3])
        data = serializers.BookSerializer(books_filterted, many=True, context=self.get_serializer_context()).data
        return Response({"highest_books": data})
    

class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()

    def get_queryset(self):
        book_id = self.request.query_params.get("book_id", None)
        if book_id is not None:
            return self.queryset.filter(book_id=book_id).order_by("-rating")
        return self.queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
  
