from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    PrimaryKeyRelatedField,
    ValidationError
)
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import Follow
from recipes.models import Recipe

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta():
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     following=obj).exists()


class FollowSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    following = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        user = self.context.get('request').user
        following_id = data['following'].id
        if Follow.objects.filter(user=user,
                                 following__id=following_id).exists():
            raise ValidationError(
                'Вы уже подписаны на этого пользователя')
        if user.id == following_id:
            raise ValidationError('Нельзя подписаться на себя')
        return data


class FollowingRecipesSerializers(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowSerializer(ModelSerializer):

    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.follower.filter(user=obj, following=request.user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            recipes = obj.recipes.all()[:(int(recipes_limit))]
        else:
            recipes = obj.recipes.all()
        context = {'request': request}
        return FollowingRecipesSerializers(recipes, many=True,
                                           context=context).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
