from typing import Union

from fastapi import FastAPI
from profileGenerator import generateProfile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/generate")
def generate():
    image_files = ["path/to/image1.jpg", "path/to/image2.jpg"]
    profile = generateProfile(image_files)
    return profile