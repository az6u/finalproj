"""CPS 310 Recipe & Meal Planner starter application."""

from recipe_utils import (
    DAYS_OF_WEEK,
    add_meal_to_plan,
    add_recipe,
    create_recipe,
    filter_by_category,
    load_config,
    load_meal_plan,
    load_recipes,
    remove_meal_from_plan,
    save_meal_plan,
    save_recipes,
    search_by_name,
)


def ask_for_number(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        answer = input(prompt).strip()
        try:
            return float(answer)
        except ValueError:
            print("Please enter a number.")


def add_recipe_from_input(recipes, recipe_file):
    """Ask the user for recipe details, then add and save the new recipe."""
    print("\nAdd a New Recipe")
    print("----------------")
    name = input("Recipe name: ")
    category = input("Category (Breakfast, Lunch, Dinner, Snack, ...): ")
    servings = int(ask_for_number("Servings: "))
    prep_time = int(ask_for_number("Prep time (minutes): "))
    cook_time = int(ask_for_number("Cook time (minutes): "))

    ingredients = []
    print("Enter ingredients. Leave the name blank when you are done.")
    while True:
        ingredient_name = input("  Ingredient name: ").strip()
        if ingredient_name == "":
            break
        quantity = ask_for_number("  Quantity: ")
        unit = input("  Unit (cup, lb, oz, ...): ").strip()
        ingredients.append({"name": ingredient_name, "quantity": quantity, "unit": unit})

    try:
        new_recipe = create_recipe(name, category, servings, prep_time, cook_time, ingredients)
        add_recipe(recipes, new_recipe)
    except ValueError as error:
        print(f"Could not add recipe: {error}")
        return

    save_recipes(recipe_file, recipes)
    print(f"'{new_recipe['name']}' was added and saved!")


def display_recipe(recipe):
    """Display one recipe in a readable format."""
    print(f"\n{recipe['name']}")
    print("-" * len(recipe["name"]))
    print(f"Category: {recipe['category']}")
    print(f"Servings: {recipe['servings']}")
    print(f"Prep time: {recipe['prep_time']} minutes")
    print(f"Cook time: {recipe['cook_time']} minutes")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"- {ingredient['quantity']} {ingredient['unit']} {ingredient['name']}")


def list_recipes(recipes):
    """Display a numbered list of recipe names."""
    if not recipes:
        print("\nNo recipes found.")
        return

    print("\nRecipes")
    print("-------")
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe['name']} ({recipe['category']})")


def choose_recipe(recipes):
    """Prompt the user to select and view a recipe."""
    list_recipes(recipes)
    if not recipes:
        return

    try:
        selection = int(input("\nEnter recipe number: "))
    except ValueError:
        print("Invalid selection.")
        return

    if selection < 1 or selection > len(recipes):
        print("Invalid selection.")
        return

    display_recipe(recipes[selection - 1])


def show_meal_plan(meal_plan):
    """Print the meal plan, one day per line."""
    print("\nWeekly Meal Plan")
    print("----------------")
    for day in DAYS_OF_WEEK:
        meals = meal_plan[day]
        if meals:
            print(f"{day}: {', '.join(meals)}")
        else:
            print(f"{day}: (nothing planned)")


def add_meal_from_input(meal_plan, recipes, meal_plan_file):
    """Ask which recipe to add to which day, then save the plan."""
    list_recipes(recipes)
    recipe_name = input("\nRecipe name to add: ")
    day = input("Day of the week: ")
    try:
        add_meal_to_plan(meal_plan, day, recipe_name, recipes)
    except ValueError as error:
        print(f"Could not add meal: {error}")
        return
    save_meal_plan(meal_plan_file, meal_plan)
    print("Meal added to your plan!")


def remove_meal_from_input(meal_plan, meal_plan_file):
    """Ask which recipe to remove from which day, then save the plan."""
    show_meal_plan(meal_plan)
    day = input("\nDay of the week: ")
    recipe_name = input("Recipe name to remove: ")
    try:
        remove_meal_from_plan(meal_plan, day, recipe_name)
    except ValueError as error:
        print(f"Could not remove meal: {error}")
        return
    save_meal_plan(meal_plan_file, meal_plan)
    print("Meal removed from your plan.")


def main():
    """Run the starter Recipe & Meal Planner."""
    config = load_config("config.json")
    recipes = load_recipes(config["recipe_file"])
    meal_plan_file = config.get("meal_plan_file", "meal_plan.json")
    meal_plan = load_meal_plan(meal_plan_file)

    while True:
        print(f"\n{config['app_title']}")
        print("=" * len(config["app_title"]))
        print("1. List all recipes")
        print("2. Search recipes by name")
        print("3. Filter recipes by category")
        print("4. View recipe details")
        print("5. Add a new recipe")
        print("6. View weekly meal plan")
        print("7. Add a recipe to the meal plan")
        print("8. Remove a recipe from the meal plan")
        print("9. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            list_recipes(recipes)
        elif choice == "2":
            term = input("Enter recipe name: ").strip()
            list_recipes(search_by_name(recipes, term))
        elif choice == "3":
            category = input("Enter category: ").strip()
            list_recipes(filter_by_category(recipes, category))
        elif choice == "4":
            choose_recipe(recipes)
        elif choice == "5":
            add_recipe_from_input(recipes, config["recipe_file"])
        elif choice == "6":
            show_meal_plan(meal_plan)
        elif choice == "7":
            add_meal_from_input(meal_plan, recipes, meal_plan_file)
        elif choice == "8":
            remove_meal_from_input(meal_plan, meal_plan_file)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()
