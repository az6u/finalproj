"""Tests for Feature 2: the weekly meal plan."""

import json

import pytest

from recipe_utils import (
    DAYS_OF_WEEK,
    add_meal_to_plan,
    create_empty_meal_plan,
    find_day,
    load_meal_plan,
    remove_meal_from_plan,
    save_meal_plan,
)

RECIPES = [
    {"name": "Chicken Alfredo", "category": "Dinner"},
    {"name": "Berry Smoothie", "category": "Snack"},
]


def test_empty_meal_plan_has_all_seven_days():
    meal_plan = create_empty_meal_plan()
    assert list(meal_plan.keys()) == DAYS_OF_WEEK
    for day in DAYS_OF_WEEK:
        assert meal_plan[day] == []


def test_find_day_accepts_any_case_and_spaces():
    assert find_day("  monday ") == "Monday"
    assert find_day("FRIDAY") == "Friday"


def test_find_day_accepts_short_name():
    assert find_day("wed") == "Wednesday"


def test_find_day_rejects_bad_day():
    with pytest.raises(ValueError):
        find_day("Funday")


def test_add_meal_to_plan_adds_recipe_to_day():
    meal_plan = create_empty_meal_plan()
    add_meal_to_plan(meal_plan, "monday", "chicken alfredo", RECIPES)
    assert meal_plan["Monday"] == ["Chicken Alfredo"]


def test_add_meal_to_plan_allows_more_than_one_meal_per_day():
    meal_plan = create_empty_meal_plan()
    add_meal_to_plan(meal_plan, "Monday", "Chicken Alfredo", RECIPES)
    add_meal_to_plan(meal_plan, "Monday", "Berry Smoothie", RECIPES)
    assert meal_plan["Monday"] == ["Chicken Alfredo", "Berry Smoothie"]


def test_add_meal_to_plan_rejects_unknown_recipe():
    meal_plan = create_empty_meal_plan()
    with pytest.raises(ValueError):
        add_meal_to_plan(meal_plan, "Monday", "Pizza", RECIPES)


def test_add_meal_to_plan_rejects_bad_day():
    meal_plan = create_empty_meal_plan()
    with pytest.raises(ValueError):
        add_meal_to_plan(meal_plan, "Someday", "Chicken Alfredo", RECIPES)


def test_remove_meal_from_plan_removes_recipe():
    meal_plan = create_empty_meal_plan()
    add_meal_to_plan(meal_plan, "Tuesday", "Berry Smoothie", RECIPES)
    remove_meal_from_plan(meal_plan, "tuesday", "berry smoothie")
    assert meal_plan["Tuesday"] == []


def test_remove_meal_from_plan_rejects_meal_not_planned():
    meal_plan = create_empty_meal_plan()
    with pytest.raises(ValueError):
        remove_meal_from_plan(meal_plan, "Tuesday", "Berry Smoothie")


def test_load_meal_plan_returns_empty_plan_when_file_missing(tmp_path):
    missing_file = tmp_path / "does_not_exist.json"
    assert load_meal_plan(missing_file) == create_empty_meal_plan()


def test_save_then_load_meal_plan_gives_same_plan(tmp_path):
    plan_file = tmp_path / "meal_plan.json"
    meal_plan = create_empty_meal_plan()
    add_meal_to_plan(meal_plan, "Sunday", "Chicken Alfredo", RECIPES)
    save_meal_plan(plan_file, meal_plan)
    assert load_meal_plan(plan_file) == meal_plan


def test_load_meal_plan_ignores_keys_that_are_not_days(tmp_path):
    plan_file = tmp_path / "meal_plan.json"
    plan_file.write_text(json.dumps({"Monday": ["Chicken Alfredo"], "Funday": ["Cake"]}))
    meal_plan = load_meal_plan(plan_file)
    assert meal_plan["Monday"] == ["Chicken Alfredo"]
    assert "Funday" not in meal_plan
