"""citext extension

Revision ID: 8664a38630eb
Revises: e495a7f5d354
Create Date: 2026-08-19 11:59:18.047239-05:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_file


# revision identifiers, used by Alembic.
revision: str = '8664a38630eb'
down_revision: Union[str, Sequence[str], None] = 'e495a7f5d354'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS citext")
