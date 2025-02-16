from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

def generateItems(input_data):
    # Load environment variables
    load_dotenv()
    serpapi_key = os.getenv("SERPAPI_KEY")

    for obj in input_data.get("outfit_recommendations", []):
        # Use description for text search instead of image URL
        description = obj.get("description", "")
        if not description:
            continue

        # Perform Google Shopping search with text
        print(description)
        params = {
            "engine": "google_shopping",
            "q": description,
            "api_key": serpapi_key,
            "num": 10
        }

        results = GoogleSearch(params).get_dict()
        shopping_results = results.get("shopping_results", [])
        
        formatted_results = []
        for item in shopping_results[:10]:
            formatted_item = {
                "name": item.get("title"),
                "link": item.get("link"),
                "price": item.get("price", "N/A"),
                "image": item.get("thumbnail"),
                "source": "Google Shopping",
                "thumbnail": item.get("thumbnail"),
            }
            formatted_results.append(formatted_item)

        return formatted_results

    return []
