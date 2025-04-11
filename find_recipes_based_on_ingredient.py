import glob
import os
import json

def find_recipes_with_ingredient(ingr):
    try:
        files = glob.glob('segregated_recipes/**/*.txt')
        recipes = list()
        recipe_dict = dict()
        for file in files:
            try:
                recipe_dict[file] = list()
                with open(file) as f:
                    for line in f.readlines():
                        if ingr in line:
                            groups = line.split(':')
                            recipe_name = groups[0].strip().rstrip().lstrip()
                            if ('.' in recipe_name):
                                recipe_name = recipe_name.split('.')[1]
                            recipes.append('Located at ' + file.replace('segregated_recipes\\','').replace('.txt','').split('\\')[1] + ' : \n' + recipe_name)
                            recipe_dict[file].append(recipe_name)
            except Exception as e:
                logging.error(f"Error processing file {file}: {e}")

        final_recipe_dict = {key: value for key, value in recipe_dict.items() if len(value) != 0}

        if not os.path.exists('searched_ingredient_recipes'):
            os.mkdir('searched_ingredient_recipes')
        with open('searched_ingredient_recipes' + os.sep + 'search_for_ingredient-' + ingr + '.txt','w+') as f:
            for recip in recipes:
                f.write(recip + '\n')

        return final_recipe_dict
    except Exception as e:
        logging.error(f"Error in find_recipes_with_ingredient: {e}")
        return {}

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
    try:
        fpath = r"segregated_recipes" + os.sep + meal_type
        files = glob.glob(fpath + os.sep + "*.txt")
        for file in files:
            try:
                with open(file) as f:
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
                              "recipe_url": recipe_url_dict}
                json_object = json.dumps(total_dict, indent=4)
                with open(fname, "w") as outfile:
                    outfile.write(json_object)
            except Exception as e:
                logging.error(f"Error processing file {file}: {e}")
    except Exception as e:
        logging.error(f"Error in create_dictionaries_for_meals: {e}")

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
        option_string = file_name.replace('.txt','')
        if option_string != '':
            available_options.append(option_string)
            available_files.append(file)
    available_option_string = ""
    for i,option in enumerate(available_options):
        available_option_string += f"{i}. {option};\n"
    #index = int(input("Select index you want : " + available_option_string))
    try:
        jf = available_files[index]
    except:
        print(meal_type)
        print(fpath)
        print(available_files)
        print("Please select a valid index,available files are : ")
        print(available_options)

    json_file = jf[:-4] + '.json'
    f = open(json_file)
    data = json.load(f)
    ingredient_dict = data["ingredients"]
    recipe_dict = data["recipe_url"]
    instr_dict = data["Recipe"]
    return ingredient_dict,recipe_dict,instr_dict    

def update_json_with_new_urls(meal_type, index, updated_url_dict):
    # Determine the JSON file path
    fpath = r"segregated_recipes" + os.sep + meal_type
    files = glob.glob(fpath + os.sep + "*.txt")
    available_files = [file for file in files if os.path.basename(file).replace('.txt', '') != '']
    
    try:
        json_file = available_files[index][:-4] + '.json'  # Get the JSON file path
    except IndexError:
        print(f"Invalid index {index}. Cannot update JSON.")
        return

    # Load the existing JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Update the recipe_url section with the new URL dictionary
    data["recipe_url"] = updated_url_dict

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Updated JSON file: {json_file}")

def add_key_value_to_json(meal_type, index, new_key, new_value):
    # Determine the JSON file path
    fpath = r"segregated_recipes" + os.sep + meal_type
    files = glob.glob(fpath + os.sep + "*.txt")
    available_files = [file for file in files if os.path.basename(file).replace('.txt', '') != '']
    
    try:
        json_file = available_files[index][:-4] + '.json'  # Get the JSON file path
    except IndexError:
        print(f"Invalid index {index}. Cannot update JSON.")
        return

    # Load the existing JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Add the new key-value pair
    data[new_key] = new_value

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Added key '{new_key}' to JSON file: {json_file}")