import json

import aiofiles


async def get_text(key: str) -> str | None:
    """
    Функция, по ключу сооющения возвращающая тект сооющения из text.json

    :param str key: ключ для получения текста из text.json
    """
    async with aiofiles.open('static/text.json', mode='r') as file:
        row_content = await file.read()

    json_content: dict[str, str] = json.loads(row_content)

    return json_content.get(key)
