import streamlit as st
import pandas as pd
import google.generativeai as genai
from recipe_api import search_recipes_by_ingredients
from translation import get_keyword, translate_recipes_steps, choose_best
from scraper import search
st.set_page_config(page_title="食材magic", layout="wide",page_icon=":material/award_meal:")
with st.sidebar:
    st.header("我的冰箱")
    spoonacular_key = st.text_input("Spoonacular API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    ingredients = st.text_area("輸入食材(英文, 用逗號分隔)", "Chicken, Tomato, Pasta")
    allergies = st.multiselect(
        "過敏原篩選",
        options=["Gluten Free", "Dairy Free", "Peanut Free", "Seafood Free", "Soy Free", "Vegetarian", "Vegan"]
    )
    limit = st.number_input("搜尋食譜數量(1-10)", min_value=1, max_value=10, value=2)
    search_btn = st.button("🔍 搜尋食譜", type="primary")
st.title("👨‍🍳讓食材煮🔥🔥🔥")
if search_btn:
    if not spoonacular_key or not gemini_key or not ingredients:
        st.error("⚠️請填寫所有必要欄位(API Keys 和食材）")
        st.stop()
    try:
        genai.configure(api_key=gemini_key)
    except Exception as e:
        st.error(f"Gemini API Key 配置失敗: {e}")
        st.stop()
    with st.spinner("正在搜尋食譜..."):
        try:
            recipes = search_recipes_by_ingredients(
                spoonacular_key, 
                ingredients, 
                limit=limit,
                allergen=allergies
            )
        except Exception as e:
            st.error(f"❌ 食譜搜尋失敗: {e}")
            st.stop()
        if not recipes:
            st.error("找不到食譜，請試著更換食材組合！")
            st.stop()
        
        with st.spinner("正在翻譯所有食譜步驟..."):
            translated_steps_dict = translate_recipes_steps(recipes)
        
        for recipe_idx, recipe in enumerate(recipes):
            st.markdown(f"## 🍲 {recipe['title']}")
            col1, col2 = st.columns([4, 5])
            with col1:
                if recipe['image']:
                    st.image(recipe['image'], width=300)
                with st.expander("📋 查看詳細步驟", expanded=False):
                    steps = recipe.get('steps', [])
                    if steps:
                        translated_steps = translated_steps_dict.get(str(recipe_idx))
                        if translated_steps:
                            for i, step in enumerate(translated_steps, 1):
                                st.write(f"**{i}.** {step}")
                        else:
                            for i, step in enumerate(steps, 1):
                                st.write(f"**{i}.** {step}")
                    else:
                        st.info("此食譜未提供詳細步驟")
            with col2:
                st.subheader("🛒 採購清單 (家樂福比價)")
                miss = recipe.get('missing_ingredients', [])
                if not miss:
                    st.success("✅ 您已擁有所有食材！")
                else:
                    allnames = [item['name'] for item in miss]
                    with st.spinner("正在翻譯食材名稱..."):
                        translation_map = get_keyword(allnames)
                    cost = 0
                    shopping_list = []
                    progress_bar = st.progress(0)
                    total = len(miss)
                    for id, item in enumerate(miss):
                        eng_name = item['name']
                        keyword = translation_map.get(eng_name, eng_name)
                        options = search(keyword, limit=5)
                        match = choose_best(
                            eng_name, 
                            options, 
                        )

                        if match:
                            price = match['price']
                            product_name = match['title']
                            link = match['link']
                            is_on_sale = match.get('is_on_sale', False)
                            original_price = match.get('original_price', 0)
                            if is_on_sale and original_price > 0:
                                price_display = f"🔥${price}(原價:${original_price})"
                            else:
                                price_display = f"${price}"
                            cost += price
                            shopping_list.append({
                                "缺漏食材": eng_name,
                                "搜尋關鍵字": keyword,
                                "家樂福商品": f"[{product_name}]({link})",
                                "預估價格": price_display
                            })
                        else:
                            shopping_list.append({
                                "缺漏食材": eng_name,
                                "搜尋關鍵字": keyword,
                                "家樂福商品": "查無合適商品",
                                "預估價格": "-"
                            })
                        
                        progress_bar.progress((id + 1) / total)
                    if shopping_list:
                        st.markdown(pd.DataFrame(shopping_list).to_markdown(index=False))
                        st.success(f"💰 補齊食材預估總價: NT$ {cost}")
                st.subheader("📊 營養成分")
                nutrients = recipe.get('nutrition', [])
                if nutrients:
                    x = pd.DataFrame(nutrients)
                    st.bar_chart(x.set_index("name")['amount'])
                else:
                    st.info("此食譜未提供營養資訊")
            st.divider()