from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    main_menu = State()


class GetDataState(StatesGroup):
    add_comment = State()