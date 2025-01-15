"""Removed discipline_sources

Revision ID: de80639fe353
Revises: c0a8968a2b1d
Create Date: 2023-03-16 22:20:50.759021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de80639fe353'
down_revision = 'c0a8968a2b1d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_notify_settings', 'discipline_sources')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'user_notify_settings',
        sa.Column('discipline_sources', sa.BOOLEAN(), nullable=False),
    )
    # ### end Alembic commands ###