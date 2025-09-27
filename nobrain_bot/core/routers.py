from aiogram import Router

from nobrain_bot.features.common.handlers.start_bot import router as start
from nobrain_bot.features.common.handlers.fallback import router as fallback
from nobrain_bot.features.common.handlers.links import router as links

# order handlers
from nobrain_bot.features.order.handlers.start_order import router as order_start
from nobrain_bot.features.order.handlers.base_questions import router as order_base
from nobrain_bot.features.order.handlers.logo_questions import router as order_logo
from nobrain_bot.features.order.handlers.site_questions import router as order_site
from nobrain_bot.features.order.handlers.bot_questions import router as order_bot
from nobrain_bot.features.order.handlers.content_questions import router as order_content
from nobrain_bot.features.order.handlers.finalize_order import router as order_finalize
from nobrain_bot.features.order.handlers.admin_decision import router as admin_decision
from nobrain_bot.features.order.handlers.client_decision import router as client_decision



ALL_ROUTERS: tuple[Router, ...] = (
    start,
    links,

    order_start,
    order_base,
    order_logo,
    order_site,
    order_bot,
    order_content,
    order_finalize,
    admin_decision,
    client_decision,

    fallback
)


def setup_routers() -> Router:
    """
    Возвращает корневой Router и включает все роутеры в заданном порядке.
    """
    root = Router(name="root")
    for r in ALL_ROUTERS:
        root.include_router(r)
    return root
