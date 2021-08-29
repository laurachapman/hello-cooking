from unicodedata import numeric

def convert_to_decimal(i):
	if len(i) == 1:
		v = numeric(i)
	elif i[-1].isdigit():
		v = float(i)
	else:
		v = float(i[:-1]) + numeric(i[-1])
	return v

class RecipeList:
	def __init__(self, recipes=[]):
		self.recipes = recipes
		self.ingredient_dict = dict()
		self.merge_ingredients(recipes)

	def add_recipe(self, recipe):
		self.recipes.append(recipe)
		self.merge_ingredients([recipe])

	def merge_ingredients(self, recipes):
		for recipe in recipes:
			for ingredient in recipe.ingredients:
				if ingredient.name in self.ingredient_dict:
					self.ingredient_dict[ingredient.name] += [ingredient.get_quantity()]
				else:
					self.ingredient_dict[ingredient.name] = [ingredient.get_quantity()]

	def get_print_string(self):
		ret = "Welcome to Bootleg Hello Fresh!\n\n"
		ret += f"Your recipes:\n"
		ret += self.get_recipe_titles()
		ret += f"Ingredient list:\n"
		for ingredient in self.ingredient_dict:
			string = ", ".join(self.ingredient_dict[ingredient])
			ret += f"{ingredient} - {string}\n"
		ret += "\nHappy cooking!"
		ret += "\n\nSent to you with hello-cooking, a script by Laura Chapman: https://github.com/laurachapman/hello-cooking"
		return ret

	def print_string(self):
		print(self.get_print_string())

	def get_recipe_titles(self):
		ret = ""
		for recipe in self.recipes:
			ret += f"- {recipe.name} ({recipe.url})\n"
		ret += "\n"
		return ret

class Recipe:
	def __init__(self, name, ingredients, url):
		self.name = name.replace("&amp;", "and")
		self.ingredients = ingredients
		self.url = url

	def print_recipe(self):
		print(self.name)
		print("Ingredients:")
		for ingredient in self.ingredients:
			print(f"\t{ingredient.name} {ingredient.amount} {ingredient.unit}")
		print(f"Full recipe: {self.url}")
		print()

class Ingredient:
	def __init__(self, name, amount, unit):
		self.name = name
		self.amount = convert_to_decimal(amount)
		self.unit = unit

	def get_quantity(self):
		return f"{self.amount} {self.unit}"