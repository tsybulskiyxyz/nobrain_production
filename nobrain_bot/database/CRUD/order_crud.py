from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from nobrain_bot.database.models import Order


# создать заявку
async def create_order(session: AsyncSession, tg_user_id, services, base_answers, details):
    # Комментарий: складываем всё как есть. status = pending по умолчанию.
    order = Order(
        tg_user_id=tg_user_id,
        services=services,
        base_answers=base_answers,
        details=details,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


# получить заявку по id
async def get_order_by_id(session: AsyncSession, order_id):
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


# обновить статус (и опционально даты / причину)
async def update_order_status(session: AsyncSession, order_id, status, start_date=None, end_date=None, decline_reason=None):
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        return None

    order.status = status
    if start_date is not None:
        order.start_date = start_date
    if end_date is not None:
        order.end_date = end_date
    if decline_reason is not None:
        order.decline_reason = decline_reason

    await session.commit()
    await session.refresh(order)
    return order


# все заявки пользователя
async def get_orders_by_user(session: AsyncSession, tg_user_id):
    result = await session.execute(
        select(Order).where(Order.tg_user_id == tg_user_id).order_by(Order.created_at.desc())
    )
    return result.scalars().all()
