from aiogram_dialog import DialogManager
from aiogram.utils.formatting import Italic, Bold
from .models import model
from math import floor
from .models import Entity
def max_values(iterable):
    max_val = iterable[0]
    for item in iterable:
        if item > max_val:
            max_val = item
    return max_val
async def get_result_data(dialog_manager: DialogManager, **_kwargs):
    for k in dialog_manager.start_data.keys():
        dialog_manager.dialog_data[k] = dialog_manager.dialog_data.get(k, 0)
    res = dialog_manager.dialog_data

    res_sorted: list[tuple[str, float]] = list(res.items())
    res_sorted.sort(key=lambda x: x[1])

    res_to_ent = {}
    res_to_print = {}
    max_values = dialog_manager.start_data
    max_points = max(max_values.values())
    for i, t in enumerate(res_sorted):
        k, v = t
        res_to_ent[k] = i + 1
        scale = floor(max_points / max_values[k])
        scaled_proc = round(v / max_values[k] * scale * 100, 2)
        scaled_proc_floor = scaled_proc if scaled_proc < 100 else 100
        res_to_print[k] = Italic(scaled_proc_floor).as_markdown().replace('\\', '')

    specs = model.position_of(Entity(res_to_ent))
    opropriate_name = Bold(specs[0][0].name).as_markdown().replace('\\', '')
    opropriate_proc = round(specs[0][1] * 100, 3)

    template = f'''
Твои результаты: 
⚙️ Системы и механизмы: {res_to_print['системы и механизмы']}%
🧮 Числа и вычисления: {res_to_print['числа и вычисления']}%
🎑 Образы и визуализация: {res_to_print['образы и визуализация']}%
🤝 Люди и взаимодействие: {res_to_print['люди и взаимодействие']}%
📜 Тексты и языки: {res_to_print['тексты и языки']}%
📣 Организация и управление: {res_to_print['организация и управление']}%
📈 Продвижение: {res_to_print['продвижение']}%
💡 Разработка и создание нового: {res_to_print['разработка и создание нового']}%
🏰Структурирование и контроль: {res_to_print['структурирование и контроль']}%
🧑‍🔬 Исследование и анализ: {res_to_print['исследование и анализ']}%

'''
    template += (Bold(f"Подходящая профессия: {opropriate_name}. Она походит тебе на {opropriate_proc}%").as_markdown()
                 .replace("\\", ''))
    res_to_print["профпригодность"] = template

    return res_to_print