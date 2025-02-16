from typing import Union

from fastapi import FastAPI
from profileGenerator import generateProfile
from dotenv import load_dotenv

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
    image_files = ["./img/animeShirt.jpeg"]
    profile = generateProfile(image_files)
    return profile