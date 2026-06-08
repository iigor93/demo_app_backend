"""create workout configs table

Revision ID: 84f7e2c9a1b4
Revises: 3b8d8f6c2f81
Create Date: 2026-06-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "84f7e2c9a1b4"
down_revision: Union[str, Sequence[str], None] = "3b8d8f6c2f81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


WORKOUTS_DATA = {
    "workouts": [
        {
            "name": "Спина и бицепс",
            "alias": "back_biceps",
            "exercises": [
                "Тяга верхнего блока к груди (широкий хват)",
                "Тяга горизонтального блока к поясу",
                "Тяга в тренажёре (аналог гантели)",
                "Подъём EZ-штанги на бицепс стоя",
                "«Молотки» с гантелями",
            ],
        },
        {
            "name": "Грудь и трицепс",
            "alias": "chest_triceps",
            "exercises": [
                "Жим штанги лёжа (горизонт)",
                "Жим гантелей на наклонной скамье (30°)",
                "Сведение рук в кроссовере (вместо бабочки)",
                "Французский жим с гантелями лёжа",
                "Разгибание рук на блоке (V-рукоять)",
            ],
        },
        {
            "name": "Ноги и плечи",
            "alias": "legs_shoulders",
            "exercises": [
                "Жим ногами в тренажёре",
                "Жим гантелей сидя (или в тренажёре)",
                "Разгибание ног в тренажёре",
                "Тяга штанги к подбородку (узкий хват)",
                "Пресс (опционально)",
            ],
        },
    ]
}


def upgrade() -> None:
    """Upgrade schema."""
    workout_configs = op.create_table(
        "workout_configs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(
        workout_configs,
        [
            {
                "data": WORKOUTS_DATA,
                "active": True,
            }
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("workout_configs")
