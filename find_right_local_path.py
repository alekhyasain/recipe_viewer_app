import glob
import os
import find_recipes_based_on_ingredient as fri
import scrape_website as sw
import logging

def search_key(key):
    try:
        # Normalize the key to match file naming conventions
        normalized_key = key.lower().replace(" ", "_").replace("-", "_")
        fixate_files = glob.glob("fixate_recipes/*/*.pdf")

        for f in fixate_files:
            # Normalize the file name for comparison
            file_name = os.path.basename(f).lower().replace(" ", "_").replace("-", "_")
            if normalized_key in file_name:
                return f

        print(f"No match found for key: {key}")
        return None  # Explicitly return None if no match is found
    except Exception as e:
        logging.error(f"Error in search_key: {e}")
        return None

folders = glob.glob("segregated_recipes/*/")
meal_type_list = list()
for fpath in folders:
    meal_type = os.path.basename(os.path.normpath(fpath))
    meal_type_list.append(str(meal_type))

for meal_type in meal_type_list:
    try:
        types_of_recipes = list()
        fpath = r"segregated_recipes" + os.sep + meal_type
        print(fpath)
        files = glob.glob(fpath + os.sep + "*.txt")
        print(files)
        for file in files:
            try:
                file_name = os.path.basename(file)
                option_string = file_name.replace('.txt','').title()
                if option_string != '':
                    types_of_recipes.append(option_string)
            except Exception as e:
                logging.error(f"Error processing file {file}: {e}")

        for i, option in enumerate(types_of_recipes):
            try:
                recipe_dict, url_dict = fri.get_ingredients_recipe_url_dict(meal_type, i)
                for key, url in url_dict.items():
                    try:
                        if url and 'drive.google.com' in url:
                            url_dict[key] = search_key(key)
                    except Exception as e:
                        logging.error(f"Error processing URL {url}: {e}")

                fri.update_json_with_new_urls(meal_type, i, url_dict)
                instr_dict = {}
                for key, url in url_dict.items():
                    try:
                        if url:
                            if url.startswith("http") and 'drive.google.com' in url:
                                text = "❌ Please download the PDF file first and pass the local path instead of a Google Drive link."
                            elif url.lower().endswith('.pdf'):
                                text = sw.extract_from_pdf(url)
                            elif url.lower().endswith('.docx'):
                                text = sw.extract_from_word(url)
                            else:
                                text = sw.extract_from_html(url)
                            instr_dict[key] = text
                    except Exception as e:
                        logging.error(f"Error extracting content from URL {url}: {e}")

                fri.add_key_value_to_json(meal_type, i, "Recipe", instr_dict)
            except Exception as e:
                logging.error(f"Error processing recipe type {option}: {e}")
    except Exception as e:
        logging.error(f"Error processing meal type {meal_type}: {e}")
