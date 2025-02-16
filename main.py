from typing import Union

from fastapi import FastAPI
from profileGenerator import generateProfile
from outfitGenerator import generateOutfits
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

app = FastAPI()
load_dotenv()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/generate")
def generate():
    def get_image_files():
        import os
        img_dir = "./img"
        return [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
    image_files = get_image_files()
    profile = generateProfile(image_files)
    
    # Generate outfit recommendations
    outfits = generateOutfits(profile)
    
    return JSONResponse({
        "profile": profile,
        "outfit_recommendations": outfits
    })
    
    