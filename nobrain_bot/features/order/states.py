from aiogram.fsm.state import StatesGroup, State


class OrderStates(StatesGroup):
    # Выбор услуг
    ChoosingServices = State()

    # ===== BASE =====
    Base_About = State()
    Base_Audience = State()
    Base_Goal = State()
    Base_Timing = State()
    Base_Budget = State()

    # ===== LOGO =====
    # Логика: стиль → цвета → использование → референсы → Готово
    Logo_Idea = State()
    Logo_Style = State()
    Logo_Colors = State()
    Logo_Print = State()
    Logo_Refs = State()

    # ===== SITE =====
    # Логика: общая идея → блоки → функционал → контент → стиль → референсы → Готово
    Site_Idea = State()
    Site_Blocks = State()
    Site_Functionality = State()
    Site_Content = State()
    Site_Style = State()
    Site_Refs = State()

    # ===== BOT =====
    # Логика: тип/задача → функционал → оплата → роли → интеграции → референсы → Готово
    Bot_Type = State()
    Bot_Functionality = State()
    Bot_Payment = State()
    Bot_Notifications = State()
    Bot_Integrations = State()
    Bot_Refs = State()

    # ===== CONTENT =====
    # Логика: что нужно → площадка → стиль/подача → референсы → Готово
    Content_Type = State()
    Content_Platform = State()
    Content_Style = State()
    Content_Refs = State()


# ===== Решение по заказу =====
class DeclineStates(StatesGroup):
    WaitingReason = State()   # ожидание причины отказа


class EditStates(StatesGroup):
    WaitingDates = State()    # ожидание сроков
    WaitingBudget = State()   # ожидание бюджета
    WaitingComment = State()  # ожидание комментария

# ===== Клиентские встречные условия =====
class ClientEditStates(StatesGroup):
    WaitingDates = State()
    WaitingBudget = State()