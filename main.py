from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, JSONResponse
import httpx
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Mount the static files (HTML, CSS, JS, and images)
app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/generate-image/{animal}")
async def generate_image(animal: str):
    api_key = os.getenv("STABILITY_API_KEY")
    
    if not api_key:
        logger.error("Stability API key not found")
        raise HTTPException(status_code=500, detail="Stability API key not found")

    api_host = 'https://api.stability.ai/v2beta/stable-image/generate/core'

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_host,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "image/*"
                },
                files={"none": ''},
                data={
                    "prompt": f"A cute {animal} in a natural setting",
                    "output_format": "webp",
                },
                timeout=30.0  # Set a timeout of 30 seconds
            )

        if response.status_code != 200:
            logger.error(f"API request failed with status code {response.status_code}")
            logger.error(f"Response content: {response.content}")
            return JSONResponse(
                status_code=response.status_code,
                content={"detail": "Image generation failed", "api_response": response.text}
            )

        return Response(content=response.content, media_type="image/webp")

    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
