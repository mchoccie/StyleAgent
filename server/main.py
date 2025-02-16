from typing import Union
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from profileGenerator import generateProfile
from outfitGenerator import generateOutfits
from itemGenerator import generateItems
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/generate")
def generate_img():
    def get_image_files():
        import os

        img_dir = "./img"
        return [
            os.path.join(img_dir, f)
            for f in os.listdir(img_dir)
            if f.endswith((".jpg", ".jpeg", ".png"))
        ]

    image_files = get_image_files()
    profile = generateProfile(image_files)

    # Generate outfit recommendations
    outfits = generateOutfits(profile)

    items = generateItems(outfits)

    return JSONResponse(
        {"profile": profile, "outfit_recommendations": outfits, "items": items}
    )

@app.post("/generate")
async def generate(images: list[UploadFile] = File(...)):
    # Create img directory if it doesn't exist
    os.makedirs("img", exist_ok=True)
    
    # Save uploaded images
    image_files = []
    for image in images:
        file_path = f"img/{image.filename}"
        with open(file_path, "wb") as f:
            content = await image.read()
            f.write(content)
        image_files.append(file_path)

    try:
        # Generate profile from images
        profile = generateProfile(image_files)

        # Generate outfit recommendations
        outfits = generateOutfits(profile)

        # Generate similar items
        items = generateItems(outfits)

        # Clean up uploaded images
        for file_path in image_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        return JSONResponse({
            "profile": profile,
            "outfit_recommendations": outfits,
            "items": items
        })
    except Exception as e:
        # Clean up uploaded images in case of error
        for file_path in image_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/generate-items")
def generate_items():
    sampleOutfits = {
        "profile": {
            "Age": 20,
            "Occupation": "Student/Gamer",
            "Location": "Urban Area",
            "Hobbies": ["Gaming", "Anime/Manga", "Cosplay"],
            "Ethnicity": "Not Specified",
            "Attire Style": "Casual",
            "Style Archetype": "Youthful/Trendy",
            "Color Palette": "Black, Blue, Pink, White",
            "Influence": "Anime Culture",
        },
        "outfit_recommendations": [
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-8dPXd0hqp3Nwe5IHNXTIhprB.png?st=2025-02-16T00%3A27%3A43Z&se=2025-02-16T02%3A27%3A43Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T04%3A20%3A44Z&ske=2025-02-16T04%3A20%3A44Z&sks=b&skv=2024-08-04&sig=fUGC0ktFR1kz4BB/DYEREN3%2BOqQfZ%2BLp4JoUvYsakFM%3D",
                "description": "A comfortable black oversized graphic tee featuring a popular anime character paired with distressed denim shorts, perfect for a casual day at campus or hanging out with friends.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-EPqS9NKd63GBJ16pnR8yhX6V.png?st=2025-02-16T00%3A27%3A56Z&se=2025-02-16T02%3A27%3A56Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T05%3A03%3A16Z&ske=2025-02-16T05%3A03%3A16Z&sks=b&skv=2024-08-04&sig=o5WvBo/8yW/xfyGVH2P%2BUAUaaAL2W4s4sHDbcvRqOr4%3D",
                "description": "A vibrant pink hoodie layered over a fitted white long-sleeve shirt, combined with black joggers and white sneakers, ideal for a cozy gaming marathon or a casual stroll in the urban area.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-uda2WBxaxc1pzPtAgW7tgJR2.png?st=2025-02-16T00%3A28%3A05Z&se=2025-02-16T02%3A28%3A05Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T05%3A54%3A23Z&ske=2025-02-16T05%3A54%3A23Z&sks=b&skv=2024-08-04&sig=LPTSw39H3oZjkRNulxZNRQPUDXgsXUKfcHU3Lq/B6so%3D",
                "description": "A trendy black bomber jacket over a blue anime anime-printed t-shirt, matched with skinny jeans and chunky high-top sneakers, suitable for a night out at a cosplay event or anime convention.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-YDgpJymWOr11GHdLcvKtpnCH.png?st=2025-02-16T00%3A28%3A23Z&se=2025-02-16T02%3A28%3A23Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T06%3A37%3A36Z&ske=2025-02-16T06%3A37%3A36Z&sks=b&skv=2024-08-04&sig=18ReazqV3E0eXckafappaKooJQjuLePq0pGBdXoY/tQ%3D",
                "description": "A stylish white crop top with subtle pink accents, paired with high-waisted black skirt and combat boots, making it a great outfit for a lunch date or attending a themed party.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-gwOy0Tsxsb0qVDwKF9k9QGhp.png?st=2025-02-16T00%3A28%3A36Z&se=2025-02-16T02%3A28%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T07%3A37%3A40Z&ske=2025-02-16T07%3A37%3A40Z&sks=b&skv=2024-08-04&sig=pcx5ZXS0uwjGoMOwJYQzlwusevaTh6/kpTnwIY5rxMQ%3D",
                "description": "A relaxed-fit blue flannel shirt worn over a fitted graphic tee, teamed with black leggings and ankle boots, perfect for an easygoing day spent catching up on your favorite anime or hanging out at a local café.",
            },
        ],
        "items": [],
    }
    return generateItems(sampleOutfits)
