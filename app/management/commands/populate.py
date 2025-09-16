from django.core.management.base import BaseCommand
from django.utils import timezone
from app import models
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Seed the database with sample users and books"

    def handle(self, *args, **kwargs):
        # Create users
        for i in range(1, 6):
            email = f"user{i}@example.com"
            if not models.User.objects.filter(email=email).exists():
                user = models.User.objects.create_user(
                    username=f"user{i}",
                    email=email,
                    password="aszx1234",
                    name=f"User {i}",
                )
                
                # Make the first user (user1) a superuser
                if i == 1:
                    user.is_superuser = True
                    user.is_staff = True
                    user.is_active = True
                    user.save()
                    
                    # Create API token for the superuser
                    token, created = Token.objects.get_or_create(user=user)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"Created SUPERUSER {user.email}")
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Superuser credentials:")
                    )
                    self.stdout.write(f"  Username: {user.username}")
                    self.stdout.write(f"  Password: aszx1234")
                    self.stdout.write(f"  API Token: {token.key}")
                    self.stdout.write("-" * 50)
                else:
                    self.stdout.write(self.style.SUCCESS(f"Created user {user.email}"))
            else:
                user = models.User.objects.get(email=email)
                # If user1 already exists but is not superuser, make them one
                if i == 1 and not user.is_superuser:
                    user.is_superuser = True
                    user.is_staff = True
                    user.is_active = True
                    user.save()
                    
                    # Create API token if doesn't exist
                    token, created = Token.objects.get_or_create(user=user)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated {email} to SUPERUSER")
                    )
                    self.stdout.write(f"  API Token: {token.key}")
                else:
                    self.stdout.write(self.style.WARNING(f"User {email} already exists"))

        # Create books
        for i in range(1, 6):
            isbn = f"97800000000{i}"
            if not models.Book.objects.filter(isbn=isbn).exists():
                book = models.Book.objects.create(
                    title=f"Book Title {i}",
                    author=f"Author {i}",
                    published_date=timezone.now().date(),
                    isbn=isbn,
                )
                self.stdout.write(self.style.SUCCESS(f"Created book {book.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Book with ISBN {isbn} already exists"))
        
        self.stdout.write("-" * 50)
        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
        self.stdout.write(self.style.SUCCESS("Use these credentials in Swagger:"))
        self.stdout.write("  Basic Auth - Username: user1, Password: aszx1234")
        
        # Get the token for display
        try:
            user1 = models.User.objects.get(username="user1")
            token = Token.objects.get(user=user1)
            self.stdout.write(f"  Token Auth - Token: {token.key}")
        except:
            self.stdout.write("  Token Auth - Token not found")