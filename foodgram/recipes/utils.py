from django.http.response import HttpResponse

from .models import RecipeIngredient


def get_ingredients_list(recipes_list):
    ingredients_dict = {}
    for recipe in recipes_list:
        ingredient = RecipeIngredient.objects.filter(
            recipe=recipe.recipe).values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit',
            )
        amount = ingredient.amount
        name = ingredient.ingredient.name
        measurement_unit = ingredient.ingredient.measurement_unit
        if name not in ingredients_dict:
            ingredients_dict[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount
            }
        else:
            ingredients_dict[name]['amount'] += amount
    to_buy = []
    for item in ingredients_dict:
        to_buy.append(f'{item} - {ingredients_dict[item]["amount"]} '
                      f'{ingredients_dict[item]["measurement_unit"]} \n')
    return to_buy


def download_file_response(list_to_download, filename):
    response = HttpResponse(list_to_download, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
