import json
import os

from dotenv import load_dotenv

# load global settings from .env file before all imports
load_dotenv()

with open("data/quiz_config.json") as json_file:
    data = json.load(json_file)
    os.environ["QUIZ_CONFIG"] = json.dumps(data)
