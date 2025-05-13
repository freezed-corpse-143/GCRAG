from fastapi import FastAPI, Request
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
    config = yaml.safe_load(f)
config_model = config[MODEL_NAME]

client = None
llm_cloud_server = config['llm_cloud_server']
if MODEL_NAME in llm_cloud_server:
    client = OpenAI(api_key=config_model['api_key'], base_url=config_model['base_url'])


@app.get("/")
async def index():
    return {"message": f"Hello! This is a server for {MODEL_NAME}. " "Go to /generate/ for generation requests."}

max_tokens = config_model['max_tokens']
temperature = config_model['temperature']
stop = None


@cache.memoize()
def generate_with_llm_client(prompt, max_tokens = max_tokens, temperature=temperature, stop=stop):
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        stop=stop
    )
    result = response.choices[0].message.content
    return result

@app.post("/generate/")
async def generate(arguments: Request):
    arguments = await arguments.json()
    start_time = time.time()
    
    result = None
    if MODEL_NAME in llm_cloud_server:
        result = generate_with_llm_client(**arguments)

    end_time = time.time()
    run_time_in_seconds = end_time - start_time
    print(result)
    return {
        "generated_text": result,
        "run_time_in_seconds": run_time_in_seconds,
    }

