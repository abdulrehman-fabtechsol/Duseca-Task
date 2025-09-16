from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from app import choices

class User(AbstractUser):
    email = models.EmailField(_("Email"), unique=True, null=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
    


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='book_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    RATING_CHOICES = [(i, f"{i} Stars") for i in range(1, 6)]
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ('book_id', 'user_id')
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1, rating__lte=5),
                name="rating_constraint",
            )
        ]
        
    
    
