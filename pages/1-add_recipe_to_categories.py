import streamlit as st
import os
import glob
import json

def update_recipe_files():
    current_file = 'segregated_recipes' + os.sep + st.session_state["meal_type"] + os.sep + st.session_state["sub_meal"]
    with open(current_file + ".txt", "a") as f:
        recipe = st.session_state["recipe"]
        ingredients = st.session_state["ingredients"]
        website = st.session_state["website"]
        f.write(f"1. {recipe}({ingredients}): {website}\n")
    f = open(current_file + '.txt')
    lines = f.readlines()
    fname = current_file + ".json"
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
    st.info("Recipe submitted")
    st.session_state["recipe"] = ""
    st.session_state["ingredients"] = ""
    st.session_state["website"] = ""


recipe = "https://www.vegrecipesofindia.com/dry-fruits-ladoo-recipe/#wprm-recipe-container-138958"
meal_types = os.listdir('segregated_recipes')
st.title("Add recipe to the list of meals")
st.selectbox("Select the meal type for your recipe",key="meal_type",options=meal_types)
files = glob.glob('segregated_recipes/' +  st.session_state["meal_type"] + '/*.json')
files = [os.path.basename(file).replace('.json','') for file in files]
st.selectbox("Select the sub category of the meal:", key="sub_meal", options=files)
with st.form("my_form"):
    st.write("Add a recipe name")
    st.text_input("Recipe", key="recipe")
    st.write("Add the ingredients in the recipe")
    st.text_input("Ingredients", key="ingredients")
    st.write("Add the website for the recipe")
    st.text_input("Website", key="website")
    st.form_submit_button("Submit", on_click=update_recipe_files)
        