
from BrailleCells import BrailleCells
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "mi primer API": "pipipipipi"
    }

@app.get("/{message}")
async def root(message):
    return {
        "message": message,
        "braille": BrailleCells.str_to_braille(message)
    }

