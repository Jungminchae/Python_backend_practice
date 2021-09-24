import random
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import Product, User
from .serializers import ProductSerializer


class ProductViewsets(ViewSet):
    # /api/products
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # raise_exception default => False
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 하나만 return 해주는 instance
    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({"id": user.id}, status=status.HTTP_200_OK)
