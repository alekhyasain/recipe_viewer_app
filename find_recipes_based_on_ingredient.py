import glob
import os
import json

def find_recipes_with_ingredient(ingr):
    files = glob.glob('segregated_recipes/**/*.txt')
    recipes = list()
    recipe_dict = dict()
    for file in files:
        recipe_dict[file] = list()
        f = open(file) 
        for line in f.readlines():
            if ingr in line:
                groups = line.split(':')
                recipe_name = groups[0].strip().rstrip().lstrip()
                if ('.' in recipe_name):
                    recipe_name = recipe_name.split('.')[1]
                recipes.append('Located at ' + file.replace('segregated_recipes\\','').replace('.txt','').split('\\')[1] + ' : \n' + recipe_name)
                recipe_dict[file].append(recipe_name)
    final_recipe_dict = {}
    for key in recipe_dict.keys():
        if len(recipe_dict[key]) != 0:
            final_recipe_dict[key] = recipe_dict[key]
    
    if not os.path.exists('searched_ingredient_recipes'):
        os.mkdir('searched_ingredient_recipes')
    f = open('searched_ingredient_recipes' + os.sep + 'search_for_ingredient-' + ingr + '.txt','w+')
    for recip in recipes:
        f.write(recip + '\n')

    return final_recipe_dict

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def find_recipes_with_max_matched_ingredients(ingr_list):
    files = glob.glob('segregated_recipes/**/*.txt')
    ingr_dict = dict()
    location_dict = dict()

    for ingr in ingr_list:
        ingr_dict[ingr] = list()
        for file in files:
            f = open(file) 
            for line in f.readlines():
                if ':' in line:
                    if ingr in line:
                        groups = line.split(':')
                        recipe_name = groups[0].strip().rstrip().lstrip()
                        if '.' in recipe_name:
                            recipe_name = recipe_name.split('.')[1]
                        ingr_dict[ingr].append(recipe_name)
                        location_dict[recipe_name] = 'Located at ' + file.replace('segregated_recipes\\','').replace('.txt','').split('\\')[1] + ' :\n'
    intersection_recipes = ingr_dict[ingr_list[0]]
    for key in ingr_dict.keys():
        intersection_recipes = intersection(intersection_recipes,ingr_dict[key])
    for recipe in intersection_recipes:
        print(location_dict[recipe] + recipe)
    return intersection_recipes
    
# find_recipes_with_ingredient("enchilada sauce")
#find_recipes_with_max_matched_ingredients(["milk", "potato"])

def create_recipes_list_per_ingredient():
    f = open('ingredient_total_list_file.txt')
    lines = f.readlines()
    for line in lines:
        if (line != ""):
            if ('//' in line):
                line.split('//')[0]
            find_recipes_with_ingredient(line.strip())

#create_recipes_list_per_ingredient()

def create_dictionaries_for_meals(meal_type):
    fpath = r"segregated_recipes" + os.sep + meal_type
    files = glob.glob(fpath + os.sep + "*.txt")
    for file in files:
        print(file)
        f = open(file)
        lines = f.readlines()
        fname = file[:-4] + ".json"
        ingredient_dict = dict()
        recipe_url_dict = dict()
        for line in lines:
            if '(' in line:
                recipe_name = line.split("(")[0].split('.')[1].strip()
                ingredients = line.split("(")[1].split(')')[0].strip()
                recipe_url = line.split(')')[1].strip().lstrip(':').lstrip(' ')
                ingredient_dict[recipe_name] = ingredients
                recipe_url_dict[recipe_name] = recipe_url
        total_dict = {"ingredients":ingredient_dict,
                      "recipe_url": recipe_url_dict
                        }
        json_object = json.dumps(total_dict, indent=4)
        with open(fname, "w") as outfile:
            outfile.write(json_object)

meal_types = ['dessert_recipes', 
'international_lunch_and_dinner_recipes', 
'sandwich_and_burger_recipes',
'snack_recipes','soup_recipes',
'rice_millet_quinoa_dishes',
'salad_recipes',
'paratha_roti_thepla_and_raita_recipes',
'international_breakfast_recipes',
'indian_sabji_recipes',
'indian_breakfast_recipes']
# for meal in meal_types:
#     create_dictionaries_for_meals(meal)

def get_ingredients_recipe_url_dict(meal_type,index):
    fpath = r"segregated_recipes" + os.sep + meal_type
    files = glob.glob(fpath + os.sep + "*.txt")
    available_options = list()
    available_files = list()
    for file in files:
        file_name = os.path.basename(file)
        option_string = file_name.lstrip(meal_type.replace('_recipes','')).replace('.txt','').lstrip(' ')
        if option_string != '':
            available_options.append(option_string)
            available_files.append(file)
    available_option_string = ""
    for i,option in enumerate(available_options):
        available_option_string += f"{i}. {option};\n"
    #index = int(input("Select index you want : " + available_option_string))
    json_file = available_files[index][:-4] + '.json'
    f = open(json_file)
    data = json.load(f)
    ingredient_dict = data["ingredients"]
    recipe_dict = data["recipe_url"]
    return ingredient_dict,recipe_dict    
