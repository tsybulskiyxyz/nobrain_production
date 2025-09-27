from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from nobrain_bot.database.session import Base


class Order(Base):
    __tablename__ = "orders"

    # Уникальный идентификатор заявки
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Telegram ID клиента
    tg_user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)

    # Список выбранных услуг — ["logo", "site", "bot", "content"]
    services: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    # Базовые ответы (about, audience, goal, timing, budget)
    base_answers: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Детали по каждой услуге (logo/site/bot/content)
    details: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Статус заявки: pending / accepted / declined
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)

    # Причина отказа (если declined)
    decline_reason: Mapped[str | None] = mapped_column(Text)

    # Даты начала и окончания проекта (опционально)
    start_date: Mapped[datetime | None] = mapped_column(DateTime)
    end_date: Mapped[datetime | None] = mapped_column(DateTime)

    # Таймстемпы
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
