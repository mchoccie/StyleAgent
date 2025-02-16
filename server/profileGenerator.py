import os
from openai import OpenAI
import json
from typing import List, Dict, Any
import base64

def generateProfile(image_files: List[str]) -> Dict[str, Any]:
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Prepare the images for the API request
    image_messages = []
    for image_file in image_files:
        with open(image_file, 'rb') as file:
            image_messages.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64.b64encode(file.read()).decode('utf-8')}"
                }
            })
    
    # Construct the system prompt
    system_prompt = """
    Analyze the provided images and create one detailed customer profile. 
    Focus on visual cues to determine age, occupation, location, ethnicity, style, and other characteristics.
    Provide the response in a JSON format, without the code block, with the following fields:
    - Age (integer)
    - Occupation (string)
    - Location (string, based on visual context)
    - Hobbies (array of strings)
    - Ethnicity (string)
    - Attire Style (one of: Casual, Business Casual, Smart Casual, Business, Streetwear, Vintage)
    - Style Archetype (string)
    - Color Palette (string)
    - Influence (string)

    example response:
    {
    "Age": 20,
    "Occupation": "Student/Artist",
    "Location": "Urban Area",
    "Hobbies": ["Gaming", "Drawing", "Anime/Manga"],
    "Ethnicity": "Not Specified",
    "Attire Style": "Casual",
    "Style Archetype": "Youthful/Trendy",
    "Color Palette": "Black, Blue, Pink",
    "Influence": "Anime Culture"
    }
    """

    # Make the API request
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": image_messages
                }
            ],
            max_tokens=1000
        )

        print(response.choices[0].message.content)
        
        # Parse the response
        profile_data = json.loads(response.choices[0].message.content)
        
        # Validate required fields
        required_fields = ["Age", "Occupation", "Location", "Ethnicity", "Attire Style", "Style Archetype"]
        for field in required_fields:
            if field not in profile_data:
                raise ValueError(f"Missing required field: {field}")
        
        return profile_data
    
    except Exception as e:
        raise Exception(f"Error generating profile: {str(e)}")
  