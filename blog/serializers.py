from rest_framework import serializers
from .models import Course, Category, Message, Room, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
# or
#class CourseSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Course
        fields = "__all__" #['name', 'category', 'price'] 