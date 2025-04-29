from fastapi import FastAPI
from diskcache import Cache
import os
import yaml
import time
from openai import OpenAI

os.makedirs("./reader/cache", exist_ok=True)
cache = Cache("./reader/cache")

app = FastAPI()

MODEL_NAME = os.environ['MODEL_NAME']
with open("./confs/config_model.yaml") as f:
    config = yaml.safe_load(f)[MODEL_NAME]

client = None
if MODEL_NAME in ["deepseek-chat", "qwen2-7b-instruct"]:
    client = OpenAI(api_key=config['api_key'], base_url=config['base_url'])






@app.get("/")
async def index():
    return {"message": f"Hello! This is a server for {MODEL_NAME}. " "Go to /generate/ for generation requests."}



@cache.memoize()
def generate_with_llm_client(prompt: str):
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=config['max_tokens'],
        temperature=config['temperature'],
    )
    result = response.choices[0].message.content
    return result

@app.get("/generate/")
async def generate(prompt: str):
    start_time = time.time()
    
    result = None
    if MODEL_NAME == "deepseek-chat":
        result = generate_with_llm_client(prompt)

    end_time = time.time()
    run_time_in_seconds = end_time - start_time
    return {
        "generated_text": result,
        "run_time_in_seconds": run_time_in_seconds,
    }

