import requests
def search_recipes_by_ingredients(api_key, ingredients, limit, allergen=None):
    try:
        url = "https://api.spoonacular.com/recipes/complexSearch"
        par = {
            "apiKey": api_key,
            "includeIngredients": ingredients,
            "fillIngredients": "true",
            "addRecipeInformation": "true",
            "addRecipeNutrition": "true",
            "addRecipeInstructions": "true",
            "number": limit,
            "sort": "max-used-ingredients",
            "sortDirection": "desc",
            "ignorePantry": "true"
        }
        if allergen:
            aller = [x.lower().replace(' free', '').replace('free', '') for x in allergen]
            par["intolerances"] = ",".join(aller)
        response = requests.get(url,par)
        response.raise_for_status()       
        recipes = response.json().get("results", [])
        wanted = []
        for r in recipes:
            nutrition = extract_nutrition(r.get("nutrition", {}).get("nutrients", []))
            steps = extract_steps(r.get("analyzedInstructions", []))
            miss = extract_missing_ingredients(r.get("missedIngredients", []))
            used = extract_used_ingredients(r.get("usedIngredients", []))
            tmp = {
                "title": r.get("title", ""),
                "image": r.get("image", ""),
                "readyInMinutes": r.get("readyInMinutes", 0),
                "nutrition": nutrition,
                "steps": steps,
                "missing_ingredients": miss,
                "used_ingredients": used
            }
            wanted.append(tmp)
        return wanted
    except requests.exceptions.RequestException as x:
        print(f"API request failed: {x}")
        return []
    except (KeyError, ValueError) as x:
        print(f"Error processing API response: {x}")
        return []
    except Exception as x:
        print(f"Unexpected error: {x}")
        return []
    
def extract_nutrition(nutrients):
    nutrition = []
    target = ["Calories", "Protein", "Fat", "Carbohydrates"]
    for nutrient in nutrients:
        if nutrient.get("name") in target:
            tmp = {
                "name": nutrient.get("name", ""),
                "amount": nutrient.get("amount", 0),
                "unit": nutrient.get("unit", "")
            }
            nutrition.append(tmp)
    return nutrition
def extract_steps(analyzed_instructions):
    steps = []
    for instruction in analyzed_instructions:
        steps_list = instruction.get("steps", [])
        for step in steps_list:
            text = step.get("step", "")
            if text:
                steps.append(text)
    return steps
def extract_used_ingredients(used_ingredients):
    used = []
    for ingredient in used_ingredients:
        tmp = {
            "name": ingredient.get("name", ""),
            "amount": ingredient.get("amount", 0),
            "unit": ingredient.get("unit", "")
        }
        used.append(tmp)
    return used
def extract_missing_ingredients(missed_ingredients):
    miss = []
    for ingredient in missed_ingredients:
        tmp = {
            "name": ingredient.get("name", ""),
            "amount": ingredient.get("amount", 0),
            "unit": ingredient.get("unit", "")
        }
        miss.append(tmp)
    return miss