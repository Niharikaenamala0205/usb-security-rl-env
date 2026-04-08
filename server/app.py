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

# 🔥 THIS IS THE MOST IMPORTANT PART
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
    global current_state
    
    if current_state is None:
        return "⚠️ First generate user!"

    if current_state == "owner" and action == "allow":
        reward = 15
        decision = "✅ Correct Decision"
    elif current_state == "unknown" and action == "alert":
        reward = 10
        decision = "✅ Correct Decision"
    elif current_state == "suspicious" and action == "block":
        reward = 20
        decision = "✅ Correct Decision"
    else:
        reward = -20
        decision = "❌ Wrong Decision"

    return f"""
🔍 User Type: {current_state}
⚙️ Action Taken: {action}
🏆 Reward: {reward}
📊 Result: {decision}
"""

with gr.Blocks() as demo:
    gr.Markdown("# 🔐 AI USB Intrusion Detection System")

    state_output = gr.Textbox(label="User Info")
    generate_btn = gr.Button("Generate User")

    action_input = gr.Radio(["allow", "block", "alert"], label="Choose Action")
    submit_btn = gr.Button("Submit Action")

    result_output = gr.Textbox(label="Result")

    generate_btn.click(generate_user, outputs=state_output)
    submit_btn.click(take_action, inputs=action_input, outputs=result_output)


# -----------------
# RUN BOTH
# -----------------

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()
    demo.launch(server_name="0.0.0.0", server_port=7860)
