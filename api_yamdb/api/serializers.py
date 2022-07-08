from http import HTTPStatus

from django.contrib.auth import authenticate, get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, GenreTitle, Review, Comment, Title


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Forbidden username, go away.", code=HTTPStatus.BAD_REQUEST
            )
        return value


class CodeTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        try:
            user = authenticate(**attrs)
        except User.DoesNotExist:
            raise Http404
        except AttributeError:
            raise serializers.ValidationError(code=HTTPStatus.BAD_REQUEST)
        else:
            return {
                'token': str(AccessToken.for_user(user))
            }


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ['role']


class UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        # fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        # fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer()

    class Meta:
        fields = '__all__'
        model = Title

    def create(self, validated_data):
        category_slug = validated_data.pop('category')
        category = get_object_or_404(Category, slug=category_slug)
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data, category=category)
            return title
        genres_slugs = validated_data.pop('genre')
        title = Title.objects.create(**validated_data, category=category)
        for genre_slug in genres_slugs:
            current_genre_slug = genre_slug['slug']
            current_genre = get_object_or_404(Genre, slug=current_genre_slug)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['title']

    def validate_score(self, value):
        if 10 < value < 1:
            raise serializers.ValidationError(
                'Оценить произведение можно баллами от 1 до 10!')
        return value


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
