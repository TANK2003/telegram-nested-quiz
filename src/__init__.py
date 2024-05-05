import json
import os

from dotenv import load_dotenv
from jsonschema import validate

# load global settings from .env file before all imports
load_dotenv(override=True)

quiz_config_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/product.schema.json",
    "title": "Nested Quiz",
    "description": "Data for a nested quiz",
    "type": "object",
    "properties": {
        "id": {"description": "The unique identifier for a quiz", "type": "string"},
        "title": {"description": "Tile of the quiz", "type": "string"},
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description": "Title of the option"},
                    "message_to_user": {
                        "description": "Message to send to user if this option is choose",
                        "type": "string",
                    },
                    "quiz": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "description": "The unique identifier for a quiz",
                                "type": "string",
                            },
                            "title": {
                                "description": "Tile of the quiz",
                                "type": "string",
                            },
                            "message_to_user": {
                                "description": "Message to send to user if this option is choose",
                                "type": "string",
                            },
                        },
                        "required": ["id", "title"],
                    },
                },
                "required": [
                    "label",
                ],
            },
        },
    },
    "required": ["id", "title", "options"],
}

with open("data/quiz_config.json") as json_file:
    data = json.load(json_file)
    validate(instance=data, schema=quiz_config_schema)
    os.environ["QUIZ_CONFIG"] = json.dumps(data)
