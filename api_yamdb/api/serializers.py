from rest_framework import serializers

from reviews.models import Categories, Genres, Review, Comments


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

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
        model = Comments
        fields = '__all__'
