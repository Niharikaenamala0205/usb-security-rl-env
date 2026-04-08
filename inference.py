import os
from openai import OpenAI

API_KEY = os.environ["API_KEY"]
API_BASE_URL = os.environ["API_BASE_URL"]
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
ENV_URL = os.getenv("ENV_URL", "https://niharikaenamala-usb-security-rl-env.hf.space")

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

import requests

TASKS = ["task_easy", "task_medium", "task_hard"]

for task in TASKS:
    print(f"[START] task={task} env=usb-security model={MODEL_NAME}", flush=True)
    try:
        requests.post(f"{ENV_URL}/reset")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"You are a USB security agent. Task: {task}. Choose: allow, block, or alert."}],
            max_tokens=50
        )
        action = response.choices[0].message.content.strip()
        result = requests.post(f"{ENV_URL}/step", json={"action": action}).json()
        raw_reward = result.get("reward", 0)
        score = max(0.01, min(0.99, (raw_reward + 20) / 40))
        print(f"[STEP] step=1 action={action} reward={score:.2f} done=true error=null", flush=True)
        print(f"[END] task={task} score={score:.2f} steps=1", flush=True)
    except Exception as e:
        print(f"[STEP] step=1 action=error reward=0.05 done=true error={str(e)[:80]}", flush=True)
        print(f"[END] task={task} score=0.05 steps=1", flush=True)
