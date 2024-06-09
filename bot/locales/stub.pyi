from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    results: Results
    criteria: Criteria


class Results:
    @staticmethod
    def message(*, systems_and_mechanisms, numbers_and_calculations, images_and_visualization, people_and_interactions, texts_and_languages, organization_and_management, promotion, development_and_creation_of_new, structuring_and_control, research_and_analysis, profession, procents) -> Literal["""Твои результаты:
⚙️ Системы и механизмы: { $systems_and_mechanisms }%
🧮 Числа и вычисления: { $numbers_and_calculations }%
🎑 Образы и визуализация: { $images_and_visualization }%
🤝 Люди и взаимодействие: { $people_and_interactions }%
📜 Тексты и языки: { $texts_and_languages }%
📣 Организация и управление: { $organization_and_management }%
📈 Продвижение: { $promotion }%
💡 Разработка и создание нового: { $development_and_creation_of_new }%
🏰Структурирование и контроль: { $structuring_and_control }%
🧑‍🔬 Исследование и анализ: { $research_and_analysis }%

Подходящая профессия: { $profession }. Она походит тебе на { $procents }%"""]: ...


class Criteria:
    @staticmethod
    def name(*, criteria) -> Literal["""{ $criteria -&gt;
[systems_and_mechanisms] системы и механизмы
[numbers_and_calculations] числа и вычисления
[images_and_visualization] образы и визуализация
[people_and_interactions] люди и взаимодействие
[texts_and_languages] тексты и языки
[organization_and_management] организация и управление
[promotion] продвижение
[development_and_creation_of_new] разработка и создание нового
[structuring_and_control] структурирование и контроль
[research_and_analysis] исследование и анализ
*[other] этого тут не должно быть...
}"""]: ...

