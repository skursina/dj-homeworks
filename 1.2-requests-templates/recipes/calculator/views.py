from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, кг': 0.3,
        'сыр, кг': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def recipe_view(request, dish):

    recipe = DATA.get(dish, {})  # получаем рецепт из DATA или пустой словарь
    
    try:
        servings = int(request.GET.get('servings', 1))  # получаем количество порций из GET-параметров
    except (ValueError, TypeError):
        servings = 1  # если передано некорректное значение, используем 1 порцию по умолчанию
        if servings < 1:
            servings = 1  # минимальное количество порций - 1

    calculated_recipe = {ingredient: quantity * servings for ingredient, quantity in recipe.items()}  # умножаем количество ингредиентов на количество порций

    context = {
        'recipe': calculated_recipe,
    }

    return render(request, 'calculator/index.html', context)