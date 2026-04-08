import random
from fastapi import FastAPI
import uvicorn

app = FastAPI()

users = ["owner", "unknown", "suspicious"]
current_state = {"value": None}

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/reset")
def reset():
    state = random.choice(users)
    current_state["value"] = state
    return {"state": state}

@app.post("/step")
def step(data: dict):
    action = data.get("action")
    state = current_state["value"]

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
