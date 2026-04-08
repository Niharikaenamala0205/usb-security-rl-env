from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# State storage
current_state = {"value": None}

# Request model (IMPORTANT)
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

# ✅ MUST be POST + accept JSON body
@app.post("/step")
def step(input: ActionInput):
    state = current_state["value"]
    action = input.action

    if state == "owner" and action == "allow":
        reward = 15
    elif state == "unknown" and action == "alert":
        reward = 10
    elif state == "suspicious" and action == "block":
        reward = 20
    else:
        reward = -20

    return {
        "state": state,
        "reward": reward,
        "done": True
    }
