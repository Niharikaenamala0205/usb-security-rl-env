import gradio as gr
from fastapi import FastAPI
from env import USBEnv

env = USBEnv()

# FastAPI app
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
# Gradio UI (optional)
# -----------------

current_state = None

def generate_user():
    global current_state
    current_state = env.reset()
    return f"User Type: {current_state}"

def take_action(action):
    global current_state
    
    if current_state is None:
        return "First generate user!"

    next_state, reward, done = env.step(action)

    return f"State: {next_state}, Reward: {reward}"


with gr.Blocks() as demo:
    gr.Markdown("# USB Security System")

    state_output = gr.Textbox(label="User Info")
    generate_btn = gr.Button("Generate User")

    action_input = gr.Radio(["allow", "block", "alert"], label="Choose Action")
    submit_btn = gr.Button("Submit Action")

    result_output = gr.Textbox(label="Result")

    generate_btn.click(generate_user, outputs=state_output)
    submit_btn.click(take_action, inputs=action_input, outputs=result_output)


app = api   
