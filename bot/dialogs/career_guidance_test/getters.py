from typing import Any, TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from bot.configs import Questions
from bot.configs.questions import QualityNameEnum
from bot.core.classification import ProfModel, Entity
from bot.utils.career_guidance_testing import prepare_model

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def questions_getter(questions: Questions, dialog_manager: DialogManager, *_args, **_kwargs):
    res: dict[str, Any] = {
        q.text: tuple(
            (
                str(i + 1),
                q.answers[i].text
            ) for i in range(len(q.answers))
        ) for q in questions.questions
    }

    state_name = dialog_manager.current_context().state.state
    res["show_previews_button"] = not state_name.endswith("question_1")

    return res


async def result_data_getter(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        prof_model: ProfModel,
        *_args,
        **_kwargs,
) -> dict[str, Any]:
    data = dialog_manager.start_data

    model = {
        "системы и механизмы": data[QualityNameEnum.systems_and_mechanisms],
        "числа и вычисления": data[QualityNameEnum.numbers_and_calculations],
        "образы и визуализация": data[QualityNameEnum.images_and_visualization],
        "люди и взаимодействие": data[QualityNameEnum.people_and_interactions],
        "тексты и языки": data[QualityNameEnum.texts_and_languages],
        "организация и управление": data[QualityNameEnum.organization_and_management],
        "продвижение": data[QualityNameEnum.promotion],
        "разработка и создание нового": data[QualityNameEnum.development_and_creation_of_new],
        "структурирование и контроль": data[QualityNameEnum.structuring_and_control],
        "исследование и анализ": data[QualityNameEnum.research_and_analysis],
    }

    prepared = Entity(prepare_model(model))
    appropriate_name, suitable_procents = prof_model.position_of(prepared)[0]

    res = {"career_guidance_test_result": i18n.results.message(
        systems_and_mechanisms=data[QualityNameEnum.systems_and_mechanisms],
        numbers_and_calculations=data[QualityNameEnum.numbers_and_calculations],
        images_and_visualization=data[QualityNameEnum.images_and_visualization],
        people_and_interactions=data[QualityNameEnum.people_and_interactions],
        texts_and_languages=data[QualityNameEnum.texts_and_languages],
        organization_and_management=data[QualityNameEnum.organization_and_management],
        promotion=data[QualityNameEnum.promotion],
        development_and_creation_of_new=data[QualityNameEnum.development_and_creation_of_new],
        structuring_and_control=data[QualityNameEnum.structuring_and_control],
        research_and_analysis=data[QualityNameEnum.research_and_analysis],

        profession=appropriate_name,
        procents=suitable_procents,
    )}

    return res
