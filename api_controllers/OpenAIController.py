from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class OpenAIClient:
    def __init__(self):
        print(os.getenv('OPENAI_API_KEY'))
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            organization=os.getenv('ORGANIZATION_ID')
        )