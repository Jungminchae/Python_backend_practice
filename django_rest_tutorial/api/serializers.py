from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


'''
Serializer
: Restful API는 JSON으로 데이터를 보내야 하는데 
  HTML로 렌더링되는 django template는 쓸 수 없음
  따라서 Queryset을 Nested한 JSON으로 매핑하는 과정을 거쳐야 함
  그것을 해주는 것이 Serializer
'''

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = (
            "id",
            'user',
            "title",
            "subtitle",
            "content",
            "created_at"
        )
        read_only_fields = ("created_at",)