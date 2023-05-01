from rest_framework import serializers
from reviews.models import (Category,
                            Comment,
                            Genre,
                            Title,
                            Review, User)
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
        model = User

    def validate_email(self, attrs):
        if attrs == self.context["request"].user:
            raise serializers.ValidationError(
                "Такой email уже зарегистрирован!"
            )
        return attrs


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, max_length=150)

    def validate_username(self, value):
        if (
            value.lower() == 'me'
        ):
            raise serializers.ValidationError(
                'Нельзя указывать me в качестве имени')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            user = User.objects.get(email=value)
            if user.username != self.initial_data.get('username'):
                raise serializers.ValidationError()
        return value


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=150, required=False)
    email = serializers.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role",
        )
        read_only_fields = ("username", "email", "role",)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug', )
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', )
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category', )


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв.'
            )
        return data


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        if not User.objects.filter(username=username).exists():
            raise NotFound("Данный пользователь не зарегистрирован")
        return data
