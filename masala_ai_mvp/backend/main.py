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
with open("recipes.json", encoding="utf-8") as f:
    RECIPES = json.load(f)

# Define ingredient keywords (customize this list as needed)
FOOD_INGREDIENTS = {
    "tomato", "onion", "green chilli", "egg", "turmeric", "tamarind", "toor dal",
    "coriander", "garlic", "ginger", "potato", "spinach", "brinjal", "eggplant",
    "cabbage", "cauliflower", "ladies finger", "okra", "ivy gourd", "ridge gourd",
    "bottle gourd", "drumstick", "malabar spinach", "black-eyed peas", "broad beans",
    "bhaji", "chukka bhaji", "peas", "chicken", "moong dal", "coconut", "cumin",
    "mustard seeds", "sambar powder", "curry leaves", "black pepper", "peanuts",
    "sesame seeds", "chilli powder", "ginger garlic paste"
}


# Initialize AWS Rekognition
rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")  # e.g. 'ap-south-1'
)

@app.post("/detect_and_suggest")
async def detect_and_suggest(file: UploadFile = File(...)):
    content = await file.read()

    # Call AWS Rekognition to detect labels
    response = rekognition.detect_labels(
        Image={"Bytes": content},
        MaxLabels=20,
        MinConfidence=70
    )

    labels = [label["Name"].lower() for label in response["Labels"]]
    detected_ingredients = [label for label in labels if label in FOOD_INGREDIENTS]

    # Score and rank recipes based on how many ingredients match
    recipe_scores = []
    for recipe in RECIPES:
        matched = [ing for ing in recipe["ingredients"] if ing.lower() in detected_ingredients]
        if matched:
            recipe_scores.append({
                "recipe": recipe,
                "match_count": len(matched),
                "total_ingredients": len(recipe["ingredients"])
            })

    # Sort recipes: most matched ingredients first, then fewer total ingredients
    sorted_recipes = sorted(
        recipe_scores,
        key=lambda x: (-x["match_count"], x["total_ingredients"])
    )

    # Extract final matching recipes
    matching_recipes = [entry["recipe"] for entry in sorted_recipes]

    return {
        "detected_ingredients": detected_ingredients,
        "recipes": matching_recipes
    }
