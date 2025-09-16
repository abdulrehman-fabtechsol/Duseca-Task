from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from app import views

router = routers.DefaultRouter()
router.register(r"user", views.UserViewSet, "user")
router.register(r"book", views.BooksViewSet, "book")
router.register(r"review", views.ReviewsViewSet, "review")


urlpatterns = [
    path("login/", obtain_auth_token, name="api_token_auth"),
    path("", include(router.urls)),
]
