import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_AI = os.getenv("USE_AI", "false").lower() == "true"