from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


class CategorySerializer123(serializers.ModelSerializer):
    pass
