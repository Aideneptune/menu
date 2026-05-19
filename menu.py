import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Receptkereső",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Recept adatbázis ---
recipes = {
    "Spaghetti Carbonara": ["spaghetti", "tojás", "bacon", "parmezán sajt", "fekete bors"],
    "Rántotta": ["tojás", "tej", "vaj", "só", "bors"],
    "Sonkás szendvics": ["kenyér", "sonka", "sajt", "saláta", "paradicsom"],
    "Paradicsomleves": ["paradicsom", "hagyma", "fokhagyma", "zöldség alaplé", "tejszín", "só", "bors"],
    "Csirke stir-fry": ["csirkemell", "brokkoli", "répa", "szójaszósz", "rizs", "gyömbér", "fokhagyma"],
    "Palacsinta": ["liszt", "tojás", "tej", "cukor", "sütőpor", "vaj"],
    "Cézár saláta": ["római saláta", "csirkemell", "pirítós", "parmezán sajt", "cézár öntet"],
    "Gombás rizottó": ["rizs", "gomba", "hagyma", "fokhagyma", "zöldség alaplé", "parmezán sajt", "fehér bor", "vaj"],
    "Tonhal saláta": ["konzerv tonhal", "majonéz", "zeller", "hagyma", "kenyér"],
    "Lencseleves": ["lencse", "répa", "zeller", "hagyma", "zöldség alaplé", "fokhagyma", "paradicsompüré"],
    "Pizza": ["pizza tészta", "paradicsomszósz", "mozzarella sajt", "pepperoni", "gomba", "olajbogyó"],
    "Chili con Carne": ["darált hús", "bab", "paradicsom", "hagyma", "fokhagyma", "chili por", "kömény", "rizs"],
    "Taco": ["taco héj", "darált hús", "saláta", "paradicsom", "sajt", "salsa", "tejföl"],
    "Lazac filé": ["lazac filé", "spárga", "citrom", "vaj", "só", "bors"],
    "Sült krumpli": ["burgonya", "olaj", "só"],
    "Zöldség curry": ["kókusztej", "curry paszta", "brokkoli", "répa", "paprika", "rizs"],
    "Quesadilla": ["tortilla", "sajt", "csirkemell", "paprika", "hagyma"],
    "Muffin": ["liszt", "tojás", "tej", "cukor", "sütőpor", "olaj", "áfonya"],
    "Brownie": ["liszt", "tojás", "vaj", "cukor", "kakaópor", "csokoládé"],
    "Sült csirkecomb": ["csirkecomb", "burgonya", "répa", "hagyma", "fokhagyma", "rozmaring", "só", "bors", "olaj"],
}

# --- Összes egyedi alapanyag gyűjtése ---
all_ingredients = sorted(list(set(ing for ingredients in recipes.values() for ing in ingredients)))

# --- Alkalmazás címe és leírása ---
st.title("Mi van a hűtőben? 🍳")
st.markdown("""
Üdvözöllek a Receptkereső alkalmazásban!
Válaszd ki azokat az alapanyagokat, amik jelenleg a hűtődben vannak,
és én megmondom, milyen ételeket tudsz belőlük készíteni,
vagy mi hiányzik hozzájuk!
""")

# --- Alapanyag választó ---
st.subheader("Válaszd ki a rendelkezésre álló alapanyagokat:")
available_ingredients = st.multiselect(
    "Alapanyagok listája",
    all_ingredients,
    placeholder="Kezdj el gépelni, vagy válassz a listából..."
)

# --- Receptkereső logika ---
if available_ingredients:
    st.subheader("Eredmények:")

    # Kategóriák a recepteknek
    can_make_now = []
    missing_1 = []
    missing_2 = []
    missing_3 = []
    missing_4_plus = []

    # Bolti lista
    shopping_list = set()

    for recipe_name, required_ingredients in recipes.items():
        required_set = set(required_ingredients)
        available_set = set(available_ingredients)

        missing = required_set - available_set
        num_missing = len(missing)

        recipe_info = {
            "name": recipe_name,
            "missing_count": num_missing,
            "missing_ingredients": list(missing)
        }

        if num_missing == 0:
            can_make_now.append(recipe_info)
        elif num_missing == 1:
            missing_1.append(recipe_info)
            shopping_list.update(missing)
        elif num_missing == 2:
            missing_2.append(recipe_info)
            shopping_list.update(missing)
        elif num_missing == 3:
            missing_3.append(recipe_info)
            shopping_list.update(missing)
        else:
            missing_4_plus.append(recipe_info)
            shopping_list.update(missing)

    # --- Eredmények megjelenítése ---

    # Elkészíthető ételek
    if can_make_now:
        st.success("🎉 Azonnal elkészíthető ételek:")
        for recipe in can_make_now:
            st.write(f"- **{recipe['name']}**")
    else:
        st.info("Nincs olyan étel, amit azonnal el tudnál készíteni a kiválasztott alapanyagokból.")

    # Hiányzó alapanyagok szerinti csoportosítás
    st.markdown("---")
    st.subheader("Ételek, amikhez hiányzik néhány alapanyag:")

    if missing_1:
        with st.expander(f"Hiányzik 1 alapanyag ({len(missing_1)} recept)"):
            for recipe in missing_1:
                st.write(f"- **{recipe['name']}**: Hiányzik: {', '.join(recipe['missing_ingredients'])}")
    if missing_2:
        with st.expander(f"Hiányzik 2 alapanyag ({len(missing_2)} recept)"):
            for recipe in missing_2:
                st.write(f"- **{recipe['name']}**: Hiányzik: {', '.join(recipe['missing_ingredients'])}")
    if missing_3:
        with st.expander(f"Hiányzik 3 alapanyag ({len(missing_3)} recept)"):
            for recipe in missing_3:
                st.write(f"- **{recipe['name']}**: Hiányzik: {', '.join(recipe['missing_ingredients'])}")
    if missing_4_plus:
        with st.expander(f"Hiányzik 4 vagy több alapanyag ({len(missing_4_plus)} recept)"):
            for recipe in missing_4_plus:
                st.write(f"- **{recipe['name']}**: Hiányzik: {', '.join(recipe['missing_ingredients'])}")

    # Bolti lista
    if shopping_list:
        st.markdown("---")
        st.subheader("🛒 Bolti lista a hiányzó alapanyagokból:")
        for item in sorted(list(shopping_list)):
            st.write(f"- {item.capitalize()}")
    else:
        st.info("Nincs szükség bevásárlásra a kiválasztott receptekhez!")

else:
    st.info("Kérlek, válassz alapanyagokat a listából a kezdéshez!")

st.markdown("---")
st.markdown("Készítette: Gemini Code Assist")
