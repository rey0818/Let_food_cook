import json
import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
path = __file__.replace("translation.py", "ingredients_dict.json")
def loading():
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print('Error loading translation data.')
        return {}
def save(data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        print('Error saving translation data.')
data = loading()

def get_keyword(ingrdients):
    if not ingrdients:
        return {}
    unique = list(set([x.strip() for x in ingrdients if x.strip()]))
    mp = {}
    miss = []
    for ingredient in unique:
        voc = ingredient.lower()
        if voc in data:
            mp[ingredient] = data[voc]
        else:
            miss.append(ingredient)
    if not miss:
        return mp
    try:
        need = "', '".join(miss)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        prompt = f"""
        Convert the following ingredient names into the core ingredient nouns commonly used in Taiwanese supermarkets (Traditional Chinese).
        
        Ingredients: '{need}'
        
        Rules:
        1. Return only 1-4 Chinese characters, without adjectives or descriptors (e.g., diced, chopped, canned, frozen, powdered).
        2. Use wording commonly seen in Taiwan supermarkets. Do NOT use Mainland China terms or academic terminology.
        Examples:
        bell pepper → 青椒 (not 甜椒)
        cilantro → 香菜 (not 芫荽)
        scallion → 蔥 (not 青蔥)
        cumin → 孜然 (not 小茴香)
        3. Do not transliterate. Do not invent words that do not exist in Taiwan's food products.
        4. For processed forms, extract the underlying ingredient:
        diced tomatoes → 番茄
        garlic powder → 大蒜
        onion flakes → 洋蔥
        5. Output as a valid JSON object with ingredient names as keys and translations as values, with no additional text.
        
        Return ONLY the JSON object in this format:
        {{"Garlic": "大蒜", "Canned Tomatoes": "番茄"}}
        """
        response = model.generate_content(prompt)
        want = response.text.strip()
        try:
            if want.startswith("```"):
                want = want.split("```")[1]
                if want.startswith("json"):
                    want = want[4:]
            want = want.strip()
            result = json.loads(want)
            for ingredient in miss:
                if ingredient in result:
                    new_voc = result[ingredient]
                    mp[ingredient] = new_voc
                    data[ingredient.lower()] = new_voc
                else:
                    mp[ingredient] = ingredient
            save(data)
            print(f"成功翻譯：{len(result)}個食材")
        except json.JSONDecodeError as x:
            print(f"翻譯食材中的JSON解析失敗: {x}")
            for ingredient in miss:
                mp[ingredient] = ingredient
    except Exception as x:
        print(f"翻譯食材中的Gemini 錯誤: {x}")
        for ingredient in miss:
            mp[ingredient] = ingredient
    
    return mp
def translate_recipes_steps(recipes):
    if not recipes:
        return {}
    try:
        text = ""
        mp = {}
        for id, recipe in enumerate(recipes):
            steps = recipe.get('steps', [])
            if steps:
                mp[str(id)] = steps
                text += f"\n【食譜 {id}: {recipe.get('title', 'Recipe')}】\n"
                for i, step in enumerate(steps, 1):
                    text += f"{i}. {step}\n"
        if not text.strip():
            return {}
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        prompt = f"""
        Translate the following cooking steps from English to Traditional Chinese (Taiwan).
        Keep the recipe numbers and step numbers.
        Maintain the same structure and order.
        
        Steps to translate:
        {text}
        
        Return ONLY a valid JSON object with recipe indices as keys and arrays of translated steps as values.
        Make sure the number of steps matches the original.
        Example format:
        {{"0": ["中文步驟1", "中文步驟2"], "1": ["中文步驟1", "中文步驟2"]}}
        """
        response = model.generate_content(prompt)
        want = response.text.strip()
        try:
            if want.startswith("```"):
                want = want.split("```")[1]
                if want.startswith("json"):
                    want = want[4:]
            want = want.strip()
            result = json.loads(want)
            return result
        except json.JSONDecodeError as x:
            print(f"步驟翻譯中的JSON解析失敗: {x}")
            return mp
        
    except Exception as x:
        print(f"步驟翻譯中的Gemini錯誤: {x}")
        return {}

def choose_best(origin, option):
    if not option:
        return None
    try:
        texts = [origin] + [item['title'] for item in option]
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=texts,
            task_type="semantic_similarity"
        )
        embeddings = result['embedding']
        query_vec = np.array(embeddings[0]).reshape(1, -1)
        option_vecs = np.array(embeddings[1:])
        scores = cosine_similarity(query_vec, option_vecs)[0]
        id = int(np.argmax(scores))
        best = float(scores[id])
        if best < 0.45:
            print("相似度太低，無法匹配")
            return None
        return option[id]
    except Exception as x:
        print(f"Gemini無法embedding:{x}")
        return option[0] if option else None