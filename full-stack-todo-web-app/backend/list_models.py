import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

output_path = r"d:\github\user2\Hackathon 2\full-stack-todo-web-app\backend\model_list_output.txt"

try:
    print("Fetching models...")
    models = client.models.list()
    with open(output_path, "w") as f:
        f.write("Available models:\n")
        for model in models.data:
            f.write(f"- {model.id}\n")
    print(f"Successfully saved model list to {output_path}")
except Exception as e:
    with open(output_path, "w") as f:
        f.write(f"Error listing models: {str(e)}\n")
    print(f"Error occurred. Check {output_path}")
