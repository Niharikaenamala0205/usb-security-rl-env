import gradio as gr
from fastapi import FastAPI
from env import USBEnv

env = USBEnv()

# ✅ FastAPI
api = FastAPI()

@api.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

@api.post("/step")
def step(data: dict):
    action = data.get("action")
    next_state, reward, done = env.step(action)
    return {"state": next_state, "reward": reward, "done": done}


# -----------------
# Gradio UI
# -----------------

current_state = None

def generate_user():
    global current_state
    current_state = env.reset()
    return f"🔍 User Type: {current_state}"

def take_action(action):
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

# 🔥 THIS IS THE KEY FIX
app = gr.mount_gradio_app(api, demo, path="/")
