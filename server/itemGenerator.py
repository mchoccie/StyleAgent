import torch
from serpapi import GoogleSearch
from transformers import CLIPProcessor, CLIPModel
import os
from dotenv import load_dotenv

# Load CLIP model
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def extract_image_features(image):
    # Process the image for CLIP
    inputs = clip_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)

    return image_features


def generateItems(input_data):
    # Load environment variables
    load_dotenv()
    serpapi_key = os.getenv("SERPAPI_KEY")

    for obj in input_data.get("outfit_recommendations", []):
        # Perform Google Shopping search
        params = {
            "engine": "google_lens",
            "url": obj.get("url"),
            "api_key": serpapi_key,
        }

        print("params", params)

        results = GoogleSearch(params).get_dict()

        print("results", results)

        # Process and format results
        visual_matches = results.get("visual_matches", [])
        formatted_results = []

        for item in visual_matches[:10]:
            # Extract price value and currency if available
            price_info = item.get("price", {})
            price = price_info.get("value", "N/A")

            formatted_item = {
                "name": item.get("title"),
                "link": item.get("link"),
                "price": price,
                "image": item.get("image"),
                "source": item.get("source"),
                "thumbnail": item.get("thumbnail"),
            }
            formatted_results.append(formatted_item)

        return formatted_results

    return []
