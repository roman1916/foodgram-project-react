from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveIntegerField, TextField,
                              UniqueConstraint)

User = get_user_model()


class Ingredient(Model):
    name = CharField(
        verbose_name='Название',
        max_length=200
    )
    measurement_unit = CharField(
        verbose_name='единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(Model):
    BLUE = '#4A61DD'
    ORANGE = '#E26C2D'
    GREEN = '#49B64E'
    PURPLE = '#8775D2'
    YELLOW = '#F9A62B'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]

    name = CharField(
        verbose_name='Название',
        unique=True,
        max_length=200
    )
    color = CharField(
        verbose_name='Цвет',
        max_length=7,
        choices=COLOR_CHOICES
    )
    slug = CharField(
        verbose_name='Слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(Model):
    name = CharField(
        verbose_name='Название',
        max_length=200
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = TextField(
        verbose_name='Описание'
    )
    tags = ManyToManyField(
        Tag,
        through='RecipeTag'
    )
    ingredients = ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='RecipeIngredient'
    )
    cooking_time = PositiveIntegerField(
        verbose_name='Время готовки',
        validators=[
            MinValueValidator(
                1,
                'Время готовки не может быть нулем!'
            )
        ]
    )
    image = ImageField(
        verbose_name='Картинка',
        upload_to='recipes/'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE
    )
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        verbose_name='Ингридиент'
    )
    amount = PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в  {self.recipe}'


class RecipeTag(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE
    )
    tag = ForeignKey(
        Tag,
        on_delete=CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Теги'

    def __str__(self):
        return 'Тег рецепта'


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_user_favorite'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingList(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='purchases',
        verbose_name='Пользователь'
    )
    recipe = ForeignKey(
        Recipe,
        related_name='purchases',
        on_delete=CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique purchases user'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
