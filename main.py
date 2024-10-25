from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, JSONResponse
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import logging
from gradio_client import Client
import base64
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Mount the static files (HTML, CSS, JS, and images)
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnimalRequest(BaseModel):
    animals: list[str]

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "size": file.size,
        "content_type": file.content_type
    }

@app.post("/generate-image")
async def generate_image(request: AnimalRequest):
    animals = " and ".join(request.animals)
    prompt = f"{animals} together"

    try:
        client = Client("black-forest-labs/FLUX.1-schnell")
        #client = Client("black-forest-labs/FLUX.1-schnell")
        result = client.predict(
            prompt=prompt,
            seed=0,
            randomize_seed=True,
            width=1024,
            height=1024,
            num_inference_steps=4,
            api_name="/infer"
        )

        # The result is likely a tuple, where the first element is the image path
        if isinstance(result, tuple) and len(result) > 0:
            image_path = result[0]
            with open(image_path, "rb") as image_file:
                image_content = image_file.read()
            return Response(content=image_content, media_type="image/png")
        else:
            logger.error(f"Unexpected result format: {result}")
            raise HTTPException(status_code=500, detail="Unexpected result format from image generation")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
