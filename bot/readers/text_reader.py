import os

from pydantic import BaseModel

from bot.readers.config_reader import config


class Text(BaseModel):
    start_message: str
    start_inline_text: str
    launch_message: str

    home_message: str

    wardrobe_greeting: str
    wardrobe_header: str

    interview_header: str
    interview_greeting: str

    kitchen_greeting: str
    kitchen_header: str

    garage_greeting: str
    garage_header: str

    test_header: str

    currency_description: str


text_path = str(config.models_path) + os.sep + "text.json"
with open(text_path, 'r') as file:
    text = Text.model_validate_json(file.read())

if __name__ == "__main__":
    print(text.model_dump())
