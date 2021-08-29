from unicodedata import numeric

def convertToDecimal(i):
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
		self.mergeIngredients(recipes)

	def add_recipe(self, recipe):
		self.recipes.append(recipe)
		self.mergeIngredients([recipe])

	def mergeIngredients(self, recipes):
		for recipe in recipes:
			for ingredient in recipe.ingredients:
				if ingredient.name in self.ingredient_dict:
					self.ingredient_dict[ingredient.name] += [ingredient.getQuantity()]
				else:
					self.ingredient_dict[ingredient.name] = [ingredient.getQuantity()]

	def getPrintString(self):
		ret = "Welcome to Bootleg Hello Fresh!\n\n"
		ret += f"Your recipes:\n"
		ret += self.getRecipeTitles()
		ret += f"Ingredient list:\n"
		for ingredient in self.ingredient_dict:
			string = ", ".join(self.ingredient_dict[ingredient])
			ret += f"{ingredient} - {string}\n"
		ret += "\nHappy cooking!"
		ret += "\n\nSent to you with hello-cooking, a script by Laura Chapman: https://github.com/laurachapman/hello-cooking"
		return ret

	def printIngredients(self):
		print(self.getPrintString())

	def getRecipeTitles(self):
		ret = ""
		for recipe in self.recipes:
			ret += f"- {recipe.name} ({recipe.url})\n"
		ret += "\n"
		return ret

	def printRecipeTitles(self):
		print(self.getRecipeTitles())

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
		self.amount = convertToDecimal(amount)
		self.unit = unit

	def getQuantity(self):
		return f"{self.amount} {self.unit}"