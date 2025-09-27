from alembic import op
import sqlalchemy as sa
# Если хочешь JSONB:
# from sqlalchemy.dialects import postgresql as psql

revision = 'a4513a79bc6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("tg_user_id", sa.BigInteger, nullable=False),
        # Если хочешь JSONB, замени sa.JSON на psql.JSONB
        sa.Column("services", sa.JSON, nullable=False),
        sa.Column("base_answers", sa.JSON, nullable=False),
        sa.Column("details", sa.JSON, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("decline_reason", sa.Text, nullable=True),
        sa.Column("start_date", sa.DateTime, nullable=True),
        sa.Column("end_date", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    # Индексы отдельно:
    op.create_index("ix_orders_tg_user_id", "orders", ["tg_user_id"])
    op.create_index("ix_orders_status", "orders", ["status"])


def downgrade() -> None:
    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_index("ix_orders_tg_user_id", table_name="orders")
    op.drop_table("orders")
