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
