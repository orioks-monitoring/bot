"""Initial migration

Revision ID: e09d97658b84
Revises: 
Create Date: 2022-06-14 04:37:58.451042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e09d97658b84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'admin_statistics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('scheduled_requests', sa.Integer(), nullable=False),
        sa.Column('success_logins', sa.Integer(), nullable=False),
        sa.Column('failed_logins', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'user_notify_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_telegram_id', sa.Integer(), nullable=False),
        sa.Column('marks', sa.Boolean(), nullable=False),
        sa.Column('news', sa.Boolean(), nullable=False),
        sa.Column('discipline_sources', sa.Boolean(), nullable=False),
        sa.Column('homeworks', sa.Boolean(), nullable=False),
        sa.Column('requests', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'user_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_telegram_id', sa.Integer(), nullable=False),
        sa.Column('agreement_accepted', sa.Boolean(), nullable=False),
        sa.Column('authenticated', sa.Boolean(), nullable=False),
        sa.Column('login_attempt_count', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_status')
    op.drop_table('user_notify_settings')
    op.drop_table('admin_statistics')
    # ### end Alembic commands ###