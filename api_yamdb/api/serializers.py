from rest_framework import serializers
from reviews.models import Title, Genre, Category, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        read_only_fields = 'slug'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        read_only_fields = 'slug'
        model = Category


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
