# pylint: disable=missing-docstring,line-too-long,fixme
import sys
from os import path
import csv
import requests
from bs4 import BeautifulSoup


def parse(html):
    #import pdb; pdb.set_trace()
    # TODO: return a list of dict {name, difficulty, prep_time}
    soup = BeautifulSoup(html, "html.parser")
    recipe_names = soup.find_all('p', class_= 'recipe-name')
    recipe_cooktimes = soup.find_all('span', class_= 'recipe-cooktime')
    recipe_difficulties = soup.find_all('span', class_= 'recipe-difficulty')
    recipe_list =[]
    for name, cooktime, difficulty in zip(recipe_names, recipe_cooktimes, recipe_difficulties):
        recipe_list.append({"name" : name.text, "difficulty" : difficulty.text, "prep_time" : cooktime.text})
    return recipe_list

def write_csv(ingredient, recipes):
    #import pdb; pdb.set_trace()
    # TODO: dump recipes to a CSV file `recipes/INGREDIENT.csv`
    ingredient_file = f"recipes/{ingredient.upper()}.csv"
    with open(ingredient_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=recipes[0].keys())
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient):#, start=0):
    #import pdb; pdb.set_trace()
    # TODO: Use `requests` to get the HTML page of search results for given ingredients.
    url = f"https://recipes.lewagon.com/?search[query]={ingredient}"
    response = requests.get(url).content
    return response

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file)
    print("Please, run the following command first:")
    print(f'  curl "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    #import pdb; pdb.set_trace()
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        # TODO: Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = parse(scrape_from_internet(ingredient))
        #print(recipes)
        write_csv(ingredient, recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
