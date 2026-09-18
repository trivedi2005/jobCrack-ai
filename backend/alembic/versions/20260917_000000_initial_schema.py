"""Create the initial application schema.

Revision ID: 20260917_initial
Revises:
Create Date: 2026-09-17
"""

from alembic import op
from app.core.database import Base
from app.models import *  # noqa: F401,F403


revision = "20260917_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
