from typing import Any, TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from bot.configs import Questions
from bot.core.classification import ProfModel, Entity
from bot.utils.career_guidance_testing import prepare_model

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def questions_getter(questions: Questions, **_kwargs):
    return {
        q.text: tuple(
            (
                str(i + 1),
                q.answers[i].text
            ) for i in range(len(q.answers))
        ) for q in questions.questions
    }


async def result_data_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        prof_model: ProfModel
) -> dict[str, Any]:
    data = dialog_manager.dialog_data

    model = {
        "системы и механизмы": data["systems_and_mechanisms"],
        "числа и вычисления": data["numbers_and_calculations"],
        "образы и визуализация": data["images_and_visualization"],
        "люди и взаимодействие": data["people_and_interactions"],
        "тексты и языки": data["texts_and_languages"],
        "организация и управление": data["organization_and_management"],
        "продвижение": data["promotion"],
        "разработка и создание нового": data["development_and_creation_of_new"],
        "структурирование и контроль": data["structuring_and_control"],
        "исследование и анализ": data["research_and_analysis"],
    }

    prepared = Entity(prepare_model(model))
    appropriate_name, suitable_procents = prof_model.position_of(prepared)[0]

    res = {"proftest_results": i18n.results.message(
        systems_and_mechanisms=data["systems_and_mechanisms"],
        numbers_and_calculations=data["numbers_and_calculations"],
        images_and_visualization=data["images_and_visualization"],
        people_and_interactions=data["people_and_interactions"],
        texts_and_languages=data["texts_and_languages"],
        organization_and_management=data["organization_and_management"],
        promotion=data["promotion"],
        development_and_creation_of_new=data["development_and_creation_of_new"],
        structuring_and_control=data["structuring_and_control"],
        research_and_analysis=data["research_and_analysis"],

        profession=appropriate_name,
        procents=suitable_procents,
    )}

    return res
