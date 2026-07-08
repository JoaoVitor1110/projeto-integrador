"""add tga fields to vaga

Revision ID: d4e5f6a7b8c9
Revises: b2c3d4e5f6a7
Create Date: 2026-07-08

"""
from alembic import op
import sqlalchemy as sa

revision = 'd4e5f6a7b8c9'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('vagas') as batch_op:
        batch_op.add_column(sa.Column('prioridade', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('encaminhados', sa.Integer(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('recrutador_responsavel', sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table('vagas') as batch_op:
        batch_op.drop_column('recrutador_responsavel')
        batch_op.drop_column('encaminhados')
        batch_op.drop_column('prioridade')
