from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

response=completion(
    model="huggingface/meta-llama/Llama-3.1-8B-Instruct",
    messages=[{
        "role":"user",
        "content":"What is Machine Learning",
    }],
    api_key=os.environ.get("HUGGINGFACEHUB_API_TOKEN")
)
print(response.choices[0].message.content)
