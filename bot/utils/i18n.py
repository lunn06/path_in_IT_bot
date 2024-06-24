from fluent_compiler.bundle import FluentBundle  # type: ignore
from fluentogram import TranslatorHub, FluentTranslator  # type: ignore


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {
            "ru": ("ru",),
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=["bot/locales/ru/LC_MESSAGES/txt.ftl"])),
        ],
        root_locale="ru",
    )
    return translator_hub
