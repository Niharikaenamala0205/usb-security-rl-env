from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

current_state = {"value": None}

class ActionInput(BaseModel):
    action: str

@app.get("/")
def home():
    return {"message": "API Running"}

# ✅ MUST be POST
@app.post("/reset")
def reset():
    state = random.choice(["owner", "unknown", "suspicious"])
    current_state["value"] = state
    return {"state": state}

# ✅ MUST be POST
@app.post("/step")
def step(input: ActionInput):
    state = current_state["value"]

    return {
        "state": state,
        "reward": 10,
        "done": True
    }
