import random
import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

registry = {"taps": 0}

# --- DATA AGGREGATORS ---

async def fetch_nasa():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
            data = r.json()
            return f"Cosmic Event: {data.get('title')}. {data.get('explanation')[:180]}..."
        except:
            return "A gravitational anomaly blocked the NASA data stream."

async def fetch_wiki():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
        data = r.json()
        return data.get('extract', "The library of Babel returned a blank page.")

async def fetch_numbers():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://numbersapi.com/random/trivia?json")
        return r.json().get('text', "The numbers don't add up right now.")

# --- THE PROXY ENDPOINT ---

@app.get("/get-discovery")
async def get_discovery(response: Response):
    # CACHE-BUSTING HEADERS
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # Your original code
    registry["taps"] += 1
    
    # Check for sponsored injection
    if registry["taps"] % 10 == 0:
        return {
            "content": "Discover local history and industrial artifacts along the Heritage Rail Trail. The past is under your feet.",
            "is_sponsored": True,
            "type": "sponsor"
        }

    engines = {
        "nasa": fetch_nasa,
        "wiki": fetch_wiki,
        "numbers": fetch_numbers
    }
    key = random.choice(list(engines.keys()))
    content = await engines[key]()
    
    return {
        "content": content,
        "is_sponsored": False,
        "type": key
    }

# --- STATIC FILE SERVING ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
