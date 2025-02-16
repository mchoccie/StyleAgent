"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  # Google Search as a tool is not available in this version of the SDK.
  # Please try the new genAI SDK (https://ai.google.dev/gemini-api/docs/sdks)
  # and see the docs here (https://ai.google.dev/gemini-api/docs/grounding?lang=python#search-tool)
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("Image February 15, 2025 - 12:23PM.jpeg", mime_type="image/jpeg"),
  upload_to_gemini("Image February 15, 2025 - 12:36PM.jpeg", mime_type="image/jpeg"),
  upload_to_gemini("Image February 15, 2025 - 2:59PM.jpeg", mime_type="image/jpeg"),
  upload_to_gemini("1WZfbnxvFUlyYD9AcYbY_ljSrR_3MRA0t", mime_type="application/octet-stream"),
  upload_to_gemini("Image February 15, 2025 - 3:18PM.jpeg", mime_type="image/jpeg"),
  upload_to_gemini("Image February 15, 2025 - 3:19PM.jpeg", mime_type="image/jpeg"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "Tell me what product is in this image please",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"product_name\": \"New Balance 515\"\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Can you tell me how much a second hand New Balance 515 costs\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The cost of second-hand New Balance 515 sneakers can vary quite a bit depending on factors like condition, size, and specific style. Based on listings on eBay, you can find them for as low as $16.00 or as high as $64.95. Many pairs are listed in the $25 to $55 range.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[1],
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"product_name\": [\n    \"New Balance 515\"\n  ]\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[2],
        "Can you generate a customer profile for someone who would like to wear these shoes",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"Age\": 28,\n  \"Annual Income\": 60000,\n  \"Ethnicity\": \"Caucasian\",\n  \"Location\": \"Portland, Oregon\",\n  \"Occupation\": \"Graphic Designer\",\n  \"Hobbies\": [\n    \"Hiking\",\n    \"Photography\",\n    \"Attending local music events\",\n    \"Urban exploration\"\n  ]\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[3],
        "Can you give me a customer profile for someone who would wear outfits like this",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"Age\": 16,\n  \"Annual Income\": 0,\n  \"Ethnicity\": \"Asian\",\n  \"Location\": \"Los Angeles, California\",\n  \"Occupation\": \"Student\",\n  \"Hobbies\": [\n    \"Watching Anime\",\n    \"Reading Manga\",\n    \"Cosplaying\",\n    \"Drawing\",\n    \"Playing Video Games\"\n  ]\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[4],
        "Give me a style and customer profile for someone who would like to wear these outfits",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"Age\": 17,\n  \"Attire Style\": \"Casual\",\n  \"Ethnicity\": \"Caucasian\",\n  \"Location\": \"Austin, Texas\",\n  \"Occupation\": \"High School Student\",\n  \"Style Archetype\": \"Artsy\",\n  \"Color Palette\": \"Pastel colors with some brighter accents\",\n  \"Hobbies\": [\n    \"Watching Anime\",\n    \"Attending Anime Conventions\",\n    \"Drawing Fanart\",\n    \"Cosplaying\",\n    \"Listening to J-Pop and K-Pop\"\n  ],\n  \"Influence\": \"Popular Anime Series and Online Anime Communities\"\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[5],
        "Give me a style and customer profile for someone who would like to wear these outfits\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"Age\": 35,\n  \"Attire Style\": \"Business\",\n  \"Ethnicity\": \"Caucasian\",\n  \"Location\": \"New York, New York\",\n  \"Occupation\": \"Investment Banker\",\n  \"Style Archetype\": \"Classic\",\n  \"Color Palette\": \"Monochromatic shades of black, white, and grey.\",\n  \"Hobbies\": [\n    \"Golf\",\n    \"Fine Dining\",\n    \"Collecting Art\",\n    \"Traveling\"\n  ],\n  \"Influence\": \"Luxury Brands and High-End Fashion Magazines\"\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Find me clothing items that would fit this context and then display them to me, giving me some info about price and where I can buy it?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I can help you find clothing items to fit the context of a white dress shirt with a bow tie, often worn with black pants. This outfit is typically worn in formal or semi-formal settings. Here are some items that would fit this context:\n\n**1. Dress Shirt:**\n*   **Description:** A crisp, white dress shirt. Look for a shirt with a spread collar to accommodate the bow tie.\n*   **Where to buy:**\n    *   **Nordstrom:** Offers a range of dress shirts from various brands, including their own brand, which often provides good quality at a reasonable price.\n    *   **Macy's:** Similar to Nordstrom, Macy's carries a variety of dress shirt brands and styles.\n    *   **Amazon:** A broad selection of dress shirts at various price points.\n*   **Price range:** $30 - $150+ depending on the brand and quality.\n\n**2. Bow Tie:**\n*   **Description:** A black bow tie, either pre-tied or self-tie.\n*   **Where to buy:**\n    *   **The Tie Bar:** Specializes in ties and other men's accessories, offering a wide selection of bow ties.\n    *   **Etsy:** A great place to find unique or handmade bow ties.\n    *   **Amazon:** Offers a variety of bow ties at different price points.\n*   **Price range:** $15 - $50+ depending on the material and brand.\n\n**3. Dress Pants:**\n*   **Description:** Black dress pants, preferably wool or a wool blend. Look for a tailored fit.\n*   **Where to buy:**\n    *   **Brooks Brothers:** Known for their classic and high-quality dress pants.\n    *   **J.Crew:** Offers a good balance of style and affordability.\n    *   **Amazon:** Offers a variety of black dress pants at various price points.\n*   **Price range:** $50 - $200+ depending on the brand and material.\n\n**4. Dress Shoes:**\n*   **Description:** Black dress shoes, such as oxfords or loafers.\n*   **Where to buy:**\n    *   **Allen Edmonds:** Known for their high-quality, handcrafted dress shoes.\n    *   **Johnston & Murphy:** Offers a range of dress shoes at various price points.\n    *   **DSW:** A good place to find more affordable dress shoe options.\n*   **Price range:** $80 - $400+ depending on the brand and quality.\n\n**5. Accessories:**\n*   **Description:** Optional accessories such as a pocket square, cufflinks, or a dress watch can complete the outfit.\n*   **Where to buy:**\n    *   **Nordstrom:** Offers a range of men's accessories.\n    *   **Amazon:** A wide selection of accessories at various price points.\n    *   **Etsy:** A great place to find unique or handmade accessories.\n*   **Price range:** $10 - $100+ depending on the item and brand.\n\nPlease note that prices and availability may vary depending on the retailer and current promotions.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Can you generate images of these clothes too?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I am able to interact with images (e.g. describing or analysing them), but I am unable to generate or edit pixel-based images myself. This capability is only enabled for early testers.\n\nHowever, I can still help you by providing AI prompts that you could use with an image generation tool to create the images you need:\n\n1.  **Prompt for a white dress shirt:** \"A crisp, white dress shirt with a spread collar, neatly pressed and buttoned, studio lighting.\"\n2.  **Prompt for a bow tie:** \"A black silk bow tie, perfectly tied, elegant and classic, studio lighting.\"\n3.  **Prompt for dress pants:** \"Black wool dress pants with a tailored fit, sharp crease, professional, studio lighting.\"\n4.  **Prompt for dress shoes:** \"Black leather oxford dress shoes, polished and sleek, classic design, studio lighting.\"\n5.  **Prompt for accessories:** \"A silver dress watch on a wrist with a crisp white dress shirt sleeve and a black suit jacket, elegant, studio lighting.\"\n\nI hope this helps you create the images you need!\n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)