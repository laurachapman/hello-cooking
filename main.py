import requests
from bs4 import BeautifulSoup
import random
from recipe import Recipe
from recipe import Ingredient
from recipe import RecipeList
import smtplib, ssl
from email.message import EmailMessage
import getpass

def sendEmail(sender_email, password, receiver_email, message, subject=""):
	# Sender email address must have less secure apps enabled
	# https://www.google.com/settings/security/lesssecureapps
	msg = EmailMessage()
	msg.set_content(message)
	msg['Subject'] = subject
	msg['From'] = sender_email
	msg['To'] = receiver_email

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login(sender_email, "Pea67nut")
	server.send_message(msg)
	server.quit()

def getRecipes():
	URL = "https://www.hellofresh.com/menus/"
	text = requests.get(URL).text
	recipes = str(text).split("<h4")
	recipe_titles = []

	for recipe in recipes[1::]:
		start = recipe.find(">")+1
		end = recipe.find("</h4>")
		recipe_titles.append(recipe[start:end])
	return recipe_titles

def chooseRecipes(recipes, k=3):
	return random.sample(recipes, k)

def getRecipeUrl(recipe):
	recipe_search = "https://www.google.com/search?q=hellofresh+" + recipe.replace(" ", "+")
	text = requests.get(recipe_search).text
	links = str(text).split("<a href=\"/url?q=")
	end = links[1].find("&")
	recipe_link = links[1][0:end]
	return recipe_link	

def getIngredientList(url):
	recipe_page = requests.get(url)
	ingredients = str(recipe_page.text).split(" alt=\"")
	ingredient_list = []
	for ingredient in ingredients[3::]:
		if ingredient.startswith("Prep"):
			break
		end_name = ingredient.find("\"")
		name = ingredient[0:end_name]

		quantity = ingredient.split("\">")[2]
		end_quantity = quantity.find("<")
		quantity = quantity[0:end_quantity].split(" ")
		amount = ""
		unit = ""
		try:
			amount = quantity[0]
			unit = quantity[1]
			ingredient_list.append(Ingredient(name, amount, unit))
		except:
			pass
	return ingredient_list

while True:
    try:
        num_recipes = int(input("Enter a number of recipes: "))
    except ValueError:
        print("Try again, that wasn't a number: ")
        continue
    else:
        break

sender = input("Enter an email address with less secure apps enabled (see https://www.google.com/settings/security/lesssecureapps): ")
password = getpass.getpass(f"Enter password for sender email {sender} (won't show on screen): ")
recipient = input("Enter a recipient email: ")
print(f"Getting {num_recipes} recipes ready for {recipient}...")

my_recipe_list = RecipeList()
recipe_choices = getRecipes()
my_recipes = chooseRecipes(recipe_choices, num_recipes)

for recipe in my_recipes:
	print(f"Getting url for {recipe}")
	url = getRecipeUrl(recipe)
	print(f"Getting ingredients for {recipe}")
	ingredient_list = getIngredientList(url)
	recipe_object = Recipe(recipe, ingredient_list, url)
	my_recipe_list.add_recipe(recipe_object)

print()
print(my_recipe_list.getPrintString())

print(f"Sending your meal plan to {recipient}...")
sendEmail(sender, password, recipient, my_recipe_list.getPrintString(), "Your Hello Fresh recipes")
print("Done.")

