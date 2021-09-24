from django.urls import path
from .views import ProductViewsets, UserAPIView


urlpatterns = [
    path("products", ProductViewsets.as_view({"get": "list", "post": "create"})),
    path(
        "products/<str:pk>",
        ProductViewsets.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("user", UserAPIView.as_view()),
]
