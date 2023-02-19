from rest_framework import serializers
from posts.models import Comment, Post, Group, Follow, User
from rest_framework.validators import UniqueTogetherValidator


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Повтор',
            )
        ]

    def validate_following(self, following):
        if following == self.context['request'].user:
            raise serializers.ValidationError('Подписка на себя!')
        return following


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    group = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Group.objects.all()
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group', 'image')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
