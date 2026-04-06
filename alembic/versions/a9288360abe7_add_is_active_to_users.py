"""add is_active to users

Revision ID: a9288360abe7
Revises: 54d77c22a1c1
Create Date: 2026-04-06 18:31:58.911181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9288360abe7'
down_revision: Union[str, Sequence[str], None] = '54d77c22a1c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()))

def downgrade():
    op.drop_column('users', 'is_active')
