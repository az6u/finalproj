"""Utility functions for the Recipe & Meal Planner."""

import json


def load_config(filename):
    """Load application configuration from a JSON file."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def load_recipes(filename):
    """Load recipe data from a JSON file."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def search_by_name(recipes, search_term):
    """Return recipes whose names contain the search term."""
    search_term = search_term.lower()
    return [
        recipe
        for recipe in recipes
        if search_term in recipe["name"].lower()
    ]


def filter_by_category(recipes, category):
    """Return recipes that match the requested category."""
    category = category.lower()
    return [
        recipe
        for recipe in recipes
        if recipe["category"].lower() == category
    ]


def create_recipe(name, category, servings, prep_time, cook_time, ingredients):
    """Build a new recipe dictionary after checking that the values make sense.

    Raises ValueError with a helpful message if something is wrong.
    """
    name = name.strip()
    category = category.strip()

    if name == "":
        raise ValueError("Recipe name cannot be blank.")
    if category == "":
        raise ValueError("Category cannot be blank.")
    if servings <= 0:
        raise ValueError("Servings must be greater than 0.")
    if prep_time < 0 or cook_time < 0:
        raise ValueError("Prep time and cook time cannot be negative.")
    if len(ingredients) == 0:
        raise ValueError("A recipe needs at least one ingredient.")

    for ingredient in ingredients:
        if ingredient["name"].strip() == "":
            raise ValueError("Ingredient name cannot be blank.")
        if ingredient["quantity"] <= 0:
            raise ValueError("Ingredient quantity must be greater than 0.")

    return {
        "name": name,
        "category": category,
        "servings": servings,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "ingredients": ingredients,
    }


def add_recipe(recipes, new_recipe):
    """Add a recipe to the list unless one with the same name already exists."""
    for recipe in recipes:
        if recipe["name"].lower() == new_recipe["name"].lower():
            raise ValueError(f"A recipe named '{new_recipe['name']}' already exists.")
    recipes.append(new_recipe)
    return recipes


def save_recipes(filename, recipes):
    """Save the list of recipes to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(recipes, file, indent=2)


# ---------------------------------------------------------------------------
# Feature 2: Weekly meal plan
# ---------------------------------------------------------------------------

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def create_empty_meal_plan():
    """Return a meal plan with an empty list of recipe names for each day."""
    meal_plan = {}
    for day in DAYS_OF_WEEK:
        meal_plan[day] = []
    return meal_plan


def find_day(day):
    """Turn user input like 'monday' or ' MON ' into 'Monday'.

    Raises ValueError if the input is not a day of the week.
    """
    day = day.strip().lower()
    for real_day in DAYS_OF_WEEK:
        if real_day.lower() == day or real_day.lower()[:3] == day:
            return real_day
    raise ValueError(f"'{day}' is not a day of the week.")


def find_recipe_by_name(recipes, name):
    """Return the recipe with this exact name (ignoring case), or None."""
    name = name.strip().lower()
    for recipe in recipes:
        if recipe["name"].lower() == name:
            return recipe
    return None


def add_meal_to_plan(meal_plan, day, recipe_name, recipes):
    """Add a recipe to a day of the meal plan.

    Raises ValueError if the day or recipe is not valid.
    """
    real_day = find_day(day)
    recipe = find_recipe_by_name(recipes, recipe_name)
    if recipe is None:
        raise ValueError(f"No recipe named '{recipe_name.strip()}' was found.")
    meal_plan[real_day].append(recipe["name"])
    return meal_plan


def remove_meal_from_plan(meal_plan, day, recipe_name):
    """Remove a recipe from a day of the meal plan.

    Raises ValueError if the recipe is not planned for that day.
    """
    real_day = find_day(day)
    for planned_name in meal_plan[real_day]:
        if planned_name.lower() == recipe_name.strip().lower():
            meal_plan[real_day].remove(planned_name)
            return meal_plan
    raise ValueError(f"'{recipe_name.strip()}' is not planned for {real_day}.")


def load_meal_plan(filename):
    """Load the meal plan from a JSON file, or start a new one if the file is missing."""
    meal_plan = create_empty_meal_plan()
    try:
        with open(filename, encoding="utf-8") as file:
            saved_plan = json.load(file)
    except FileNotFoundError:
        return meal_plan

    # Only keep real days, so a broken file cannot add strange keys.
    for day in DAYS_OF_WEEK:
        if day in saved_plan:
            meal_plan[day] = saved_plan[day]
    return meal_plan


def save_meal_plan(filename, meal_plan):
    """Save the meal plan to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(meal_plan, file, indent=2)
