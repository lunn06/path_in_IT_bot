from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    main = State()


class Recommendations(StatesGroup):
    unimplemented = State()


class Practice(StatesGroup):
    unimplemented = State()


class CareerGuidanceTesting(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    question_12 = State()
    question_13 = State()
    question_14 = State()
    question_15 = State()
    question_16 = State()
    question_17 = State()
    question_18 = State()
    question_19 = State()
    question_20 = State()
    question_21 = State()
    question_22 = State()
    question_23 = State()
    question_24 = State()
    question_25 = State()

    results = State()
