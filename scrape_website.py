import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from urllib.parse import urlparse
import re
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    """Clean up ingredients or instructions by formatting spaces and symbols."""
    # Add space after unicode fractions (e.g., ½tsp → ½ tsp)
    text = re.sub(r'([¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞])([a-zA-Z])', r'\1 \2', text)
    # Add space between digit and letter (e.g., 1cup → 1 cup)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    # Add space between lowercase and uppercase letters (e.g., seedsCurry → seeds Curry)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    return text.strip()

def extract_ingredients_instructions_from_text(text):
    lines = text.split('\n')
    ingredients, instructions = [], []
    ing_flag, inst_flag = False, False

    for line in lines:
        line_clean = clean_text(line.lower())
        if 'ingredient' in line_clean:
            ing_flag, inst_flag = True, False
            continue
        elif 'instruction' in line_clean or 'method' in line_clean or 'direction' in line_clean:
            inst_flag, ing_flag = True, False
            continue
        elif line_clean.strip() == '':
            ing_flag, inst_flag = False, False
            continue

        if ing_flag:
            # Clean and filter ingredient lines
            if line_clean not in ingredients and len(line_clean) > 2:  # Avoid duplicates and very short lines
                ingredients.append(clean_text(line))
        elif inst_flag:
            # Clean and filter instruction lines
            if line_clean not in instructions and len(line_clean) > 2:  # Avoid duplicates and very short lines
                instructions.append(clean_text(line))

    # Deduplicate and clean ingredients and instructions
    ingredients = list(dict.fromkeys(ingredients))  # Removes duplicates while preserving order
    instructions = list(dict.fromkeys(instructions))  # Removes duplicates while preserving order

    # Convert lists to single-line strings
    ingredients_str = ', '.join(ingredients)  # Comma-separated
    instructions_str = '. '.join(instructions)  # Dot-separated
    return ingredients_str, instructions_str, None

import fitz  # PyMuPDF

def extract_from_pdf_simple(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from all pages
    for page in doc:
        text += page.get_text()
    doc.close()

    # Replace '\n' with ', ' to format the text
    text = text.replace('\n', ', ').strip()

    return text

import fitz  # PyMuPDF

def extract_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from all pages
    for page in doc:
        text += page.get_text()
    doc.close()

    # Replace '\n' with ', ' to format the text
    text = text.replace('\n', ', ').strip()

    # Extract ingredients and instructions
    ingredients, instructions = [], []
    is_ingredient_section = False
    is_instruction_section = False

    for line in text.split(', '):
        line = line.strip()

        # Identify sections
        if "INGREDIENTS" in line.upper():
            is_ingredient_section = True
            is_instruction_section = False
            continue
        elif any(keyword in line.upper() for keyword in ["INSTRUCTIONS", "METHOD", "DIRECTIONS"]):
            is_ingredient_section = False
            is_instruction_section = True
            continue

        # Add lines to the appropriate section
        if is_ingredient_section:
            ingredients.append(line)
        elif is_instruction_section:
            instructions.append(line)

    # Combine ingredients and instructions into a single text
    combined_text = "Ingredients: " + ', '.join(ingredients) + " Instructions: " + ', '.join(instructions)
    return combined_text

import requests
from bs4 import BeautifulSoup

def extract_from_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {url}: {e}")
        return f"❌ Error scraping {url}: {e}"

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=', ').strip()

        # Extract ingredients and instructions
        ingredients, instructions = [], []
        is_ingredient_section = False
        is_instruction_section = False

        for line in text.split(', '):
            line = line.strip()

            # Identify sections
            if "INGREDIENTS" in line.upper():
                is_ingredient_section = True
                is_instruction_section = False
                continue
            elif any(keyword in line.upper() for keyword in ["INSTRUCTIONS", "METHOD", "DIRECTIONS"]):
                is_ingredient_section = False
                is_instruction_section = True
                continue

            # Add lines to the appropriate section
            if is_ingredient_section:
                ingredients.append(line)
            elif is_instruction_section:
                instructions.append(line)

        combined_text = "Ingredients: " + ', '.join(ingredients) + " Instructions: " + ', '.join(instructions)
        return combined_text
    except Exception as e:
        logging.error(f"Error processing HTML content from {url}: {e}")
        return f"❌ Error processing HTML content from {url}: {e}"

def extract_from_html_simple(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"❌ Error scraping {url}: {e}"

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all text from the page
    text = soup.get_text(separator=', ').strip()

    return text
