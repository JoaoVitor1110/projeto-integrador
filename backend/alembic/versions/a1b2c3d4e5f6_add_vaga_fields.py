"""add data_abertura, data_fechamento, quantidade_vagas to vagas

Revision ID: a1b2c3d4e5f6
Revises: 063891927353
Create Date: 2026-07-02

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '063891927353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('vagas', sa.Column('data_abertura', sa.Date(), nullable=True))
    op.add_column('vagas', sa.Column('data_fechamento', sa.Date(), nullable=True))
    op.add_column('vagas', sa.Column('quantidade_vagas', sa.Integer(), nullable=False, server_default='1'))


def downgrade() -> None:
    op.drop_column('vagas', 'quantidade_vagas')
    op.drop_column('vagas', 'data_fechamento')
    op.drop_column('vagas', 'data_abertura')
