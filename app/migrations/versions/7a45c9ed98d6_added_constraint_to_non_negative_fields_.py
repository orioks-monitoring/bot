"""added constraint to non-negative fields and added unique to user_telegram_id field

Revision ID: 7a45c9ed98d6
Revises: de80639fe353
Create Date: 2023-11-12 20:21:52.378792

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a45c9ed98d6'
down_revision = 'de80639fe353'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_status') as batch_op:
        batch_op.create_check_constraint(
            'check_login_attempt_count_non_negative',
            'login_attempt_count >= 0',
        )
        batch_op.create_check_constraint(
            'check_failed_request_count_non_negative',
            'failed_request_count >= 0',
        )
        batch_op.create_unique_constraint(
            "unique_user_telegram_id_user_status", ['user_telegram_id']
        )

    with op.batch_alter_table('user_notify_settings') as batch_op:
        batch_op.create_unique_constraint(
            "unique_user_telegram_id_notify_settings", ['user_telegram_id']
        )

    with op.batch_alter_table('admin_statistics') as batch_op:
        batch_op.create_check_constraint(
            'check_scheduled_requests_non_negative',
            'scheduled_requests >= 0',
        )
        batch_op.create_check_constraint(
            'check_success_logins_non_negative',
            'success_logins >= 0',
        )
        batch_op.create_check_constraint(
            'check_failed_logins_non_negative',
            'failed_logins >= 0',
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_status') as batch_op:
        batch_op.drop_constraint(
            'check_failed_request_count_non_negative', type_='check'
        )
        batch_op.drop_constraint(
            'check_login_attempt_count_non_negative', type_='check'
        )
        batch_op.drop_constraint(
            "unique_user_telegram_id_user_status", type_='unique'
        )

    with op.batch_alter_table('user_notify_settings') as batch_op:
        batch_op.drop_constraint(
            "unique_user_telegram_id_notify_settings", type_='unique'
        )

    with op.batch_alter_table('admin_statistics') as batch_op:
        batch_op.drop_constraint(
            'check_failed_logins_non_negative', type_='check'
        )
        batch_op.drop_constraint(
            'check_success_logins_non_negative', type_='check'
        )
        batch_op.drop_constraint(
            'check_scheduled_requests_non_negative', type_='check'
        )

    # ### end Alembic commands ###