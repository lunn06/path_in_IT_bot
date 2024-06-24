from typing import Any, TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner  # type: ignore

from bot.configs import Questions
from bot.configs.questions import QualityNameEnum
from bot.core.classification import ProfModel, Entity
from bot.utils.career_guidance_testing import prepare_model

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def questions_getter(questions: Questions, dialog_manager: DialogManager, i18n: TranslatorRunner, *_args,
                           **_kwargs):
    res: dict[str, Any] = {
        q.text: tuple(
            (
                str(i + 1),
                q.answers[i].text
            ) for i in range(len(q.answers))
        ) for q in questions.questions
    }

    state_name = dialog_manager.current_context().state.state

    assert state_name

    res["show_previews_button"] = not state_name.endswith("question_1")

    res["preview_button"] = i18n.preview.button()
    res["next_button"] = i18n.next.button()
    res["results_button"] = i18n.results.button()

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
        e.value: data["qualities"][e.value] for e in QualityNameEnum
    }

    prepared = Entity(prepare_model(model))
    appropriate_name, suitable_procents = prof_model.position_of(prepared)[0]

    res = {
        "career_guidance_test_result": i18n.results.message(
            systems_and_mechanisms=data["qualities"][QualityNameEnum.systems_and_mechanisms],
            numbers_and_calculations=data["qualities"][QualityNameEnum.numbers_and_calculations],
            images_and_visualization=data["qualities"][QualityNameEnum.images_and_visualization],
            people_and_interactions=data["qualities"][QualityNameEnum.people_and_interactions],
            texts_and_languages=data["qualities"][QualityNameEnum.texts_and_languages],
            organization_and_management=data["qualities"][QualityNameEnum.organization_and_management],
            promotion=data["qualities"][QualityNameEnum.promotion],
            development_and_creation_of_new=data["qualities"][QualityNameEnum.development_and_creation_of_new],
            structuring_and_control=data["qualities"][QualityNameEnum.structuring_and_control],
            research_and_analysis=data["qualities"][QualityNameEnum.research_and_analysis],

            profession=appropriate_name.name,
            procents=suitable_procents,
        ),

        "menu_button": i18n.career.test.to.menu.button()
    }

    return res
