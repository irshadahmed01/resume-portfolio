from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load recipes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPE_PATH = os.path.join(BASE_DIR, "recipes.json")

with open(RECIPE_PATH, encoding="utf-8") as f:
    RECIPES = json.load(f)

# Whitelist of food ingredients (Telangana + common India-wide)
FOOD_INGREDIENTS = {
    "spinach", "fenugreek leaves", "amaranth leaves", "mustard greens", "goosefoot", "malabar spinach",
    "dill leaves", "sorrel leaves", "purslane", "drumstick leaves", "colocasia leaves", "coriander leaves",
    "mint leaves", "curry leaves", "lettuce", "cabbage", "kale", "bok choy", "tomato", "cucumber",
    "brinjal", "eggplant", "okra", "ladies finger", "green chilli", "capsicum", "bottle gourd",
    "ridge gourd", "sponge gourd", "bitter gourd", "pointed gourd", "ivy gourd", "snake gourd",
    "ash gourd", "pumpkin", "raw jackfruit", "raw banana", "plantain", "indian gooseberry", "zucchini",
    "potato", "sweet potato", "carrot", "radish", "beetroot", "turnip", "colocasia", "taro root",
    "elephant foot yam", "tapioca", "cassava", "onion", "garlic", "ginger", "turmeric", "lotus stem",
    "spring onion", "leek", "asparagus", "celery", "green peas", "french beans", "cluster beans",
    "broad beans", "cowpea pods", "drumstick", "guar beans", "cauliflower", "broccoli", "banana flower",
    "moringa flower", "pumpkin flower", "mushroom", "chicken", "egg", "toor dal", "moong dal", "coconut",
    "mustard seeds", "cumin", "sambar powder", "curry leaves", "black pepper", "peanuts", "sesame seeds",
    "chilli powder", "ginger garlic paste"
}

# Synonyms and normalizations
LABEL_SYNONYMS = {
    "brinjal": "eggplant",
    "aubergine": "eggplant",
    "okra": "ladies finger",
    "green chili": "green chilli",
    "green pepper": "green chilli",
    "bell pepper": "capsicum",
    "chili pepper": "green chilli",
    "bitter melon": "bitter gourd",
    "ridge gourd": "ridge gourd",
    "bottle gourd": "bottle gourd",
    "gourds": None,
    "leaf": None,
    "vegetable": None,
    "produce": None,
    "plant": None,
    "dish": None,
    "meal": None,

    # Indian local names → English
    "palak": "spinach",
    "methi": "fenugreek leaves",
    "thotakura": "amaranth leaves",
    "sarson": "mustard greens",
    "bathua": "goosefoot",
    "bachali": "malabar spinach",
    "gongura": "sorrel leaves",
    "chukka kura": "sorrel leaves",
    "gangavalli": "purslane",
    "payala kura": "purslane",
    "karivepaku": "curry leaves",
    "menthikura": "fenugreek leaves",
    "pudina": "mint leaves",
    "kothimeera": "coriander leaves",
    "ulligadda": "onion",
    "tamatar": "tomato",
    "dondakaya": "ivy gourd",
    "beerakaya": "ridge gourd",
    "sorakaya": "bottle gourd",
    "potlakaya": "snake gourd",
    "kakarakaya": "bitter gourd",
    "gummadikaya": "pumpkin",
    "aratikaya": "raw banana",
    "panasa": "raw jackfruit",
    "usirikaya": "indian gooseberry",
    "bangala dumpa": "potato",
    "chamadumpa": "taro root",
    "kanda gadda": "elephant foot yam",
    "mullangi": "radish",
    "batani": "green peas",
    "mulakkada": "drumstick",
    "bottle gourd (anapakaya)": "bottle gourd",
    "broad beans": "broad beans",
    "cowpeas": "cowpea pods",
    "cauliflower": "cauliflower",
    "putta godugulu": "mushroom",
    "vellulli": "garlic",
    "allam": "ginger",
    "raw jackfruit": "raw jackfruit"
}

# Initialize AWS Rekognition
rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@app.post("/detect_and_suggest")
async def detect_and_suggest(file: UploadFile = File(...)):
    print(f"\n📷 Received file: {file.filename} ({file.content_type})")

    content = await file.read()

    response = rekognition.detect_labels(
        Image={"Bytes": content},
        MaxLabels=30,
        MinConfidence=70
    )

    labels = [label["Name"].lower() for label in response["Labels"]]
    print("\n🧠 AWS Rekognition Labels:")
    for label in response["Labels"]:
        print(f" - {label['Name']} ({label['Confidence']:.1f}%)")

    normalized_labels = []
    for label in labels:
        if label in FOOD_INGREDIENTS:
            normalized_labels.append(label)
        elif label in LABEL_SYNONYMS:
            synonym = LABEL_SYNONYMS[label]
            if synonym and synonym in FOOD_INGREDIENTS:
                normalized_labels.append(synonym)

    detected_ingredients = list(set(normalized_labels))
    print(f"\n✅ Filtered Ingredients: {detected_ingredients}")

    if not detected_ingredients:
        return {
            "detected_ingredients": [],
            "recipes": [],
            "message": "No recognizable ingredients detected. Try using a clearer image."
        }

    recipe_scores = []
    for recipe in RECIPES:
        matched = [ing for ing in recipe["ingredients"] if ing.lower() in detected_ingredients]
        if matched:
            recipe_scores.append({
                "recipe": recipe,
                "match_count": len(matched),
                "total_ingredients": len(recipe["ingredients"])
            })

    sorted_recipes = sorted(
        recipe_scores,
        key=lambda x: (-x["match_count"], x["total_ingredients"])
    )

    matching_recipes = [entry["recipe"] for entry in sorted_recipes]

    return {
        "detected_ingredients": detected_ingredients,
        "recipes": matching_recipes
    }
