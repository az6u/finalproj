"""Tests for Feature 1: adding a new recipe."""

import pytest

from recipe_utils import add_recipe, create_recipe, load_recipes, save_recipes


def make_ingredients():
    return [{"name": "eggs", "quantity": 2, "unit": "whole"}]


def test_create_recipe_returns_recipe_dictionary():
    recipe = create_recipe("Scrambled Eggs", "Breakfast", 1, 2, 5, make_ingredients())
    assert recipe["name"] == "Scrambled Eggs"
    assert recipe["category"] == "Breakfast"
    assert recipe["servings"] == 1
    assert recipe["ingredients"] == make_ingredients()


def test_create_recipe_removes_extra_spaces():
    recipe = create_recipe("  Scrambled Eggs  ", " Breakfast ", 1, 2, 5, make_ingredients())
    assert recipe["name"] == "Scrambled Eggs"
    assert recipe["category"] == "Breakfast"


def test_create_recipe_rejects_blank_name():
    with pytest.raises(ValueError):
        create_recipe("   ", "Breakfast", 1, 2, 5, make_ingredients())


def test_create_recipe_rejects_zero_servings():
    with pytest.raises(ValueError):
        create_recipe("Eggs", "Breakfast", 0, 2, 5, make_ingredients())


def test_create_recipe_rejects_negative_time():
    with pytest.raises(ValueError):
        create_recipe("Eggs", "Breakfast", 1, -2, 5, make_ingredients())


def test_create_recipe_rejects_no_ingredients():
    with pytest.raises(ValueError):
        create_recipe("Eggs", "Breakfast", 1, 2, 5, [])


def test_create_recipe_rejects_bad_ingredient_quantity():
    ingredients = [{"name": "eggs", "quantity": 0, "unit": "whole"}]
    with pytest.raises(ValueError):
        create_recipe("Eggs", "Breakfast", 1, 2, 5, ingredients)


def test_add_recipe_adds_to_list():
    recipes = []
    new_recipe = create_recipe("Eggs", "Breakfast", 1, 2, 5, make_ingredients())
    add_recipe(recipes, new_recipe)
    assert recipes == [new_recipe]


def test_add_recipe_rejects_duplicate_name():
    recipes = [{"name": "Eggs", "category": "Breakfast"}]
    new_recipe = create_recipe("eggs", "Breakfast", 1, 2, 5, make_ingredients())
    with pytest.raises(ValueError):
        add_recipe(recipes, new_recipe)


def test_save_recipes_then_load_gives_same_data(tmp_path):
    recipe_file = tmp_path / "recipes.json"
    recipes = [create_recipe("Eggs", "Breakfast", 1, 2, 5, make_ingredients())]
    save_recipes(recipe_file, recipes)
    assert load_recipes(recipe_file) == recipes
