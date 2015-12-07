"""empty message

Revision ID: 93c6695f7f
Revises: None
Create Date: 2015-12-04 18:58:07.244222

"""

# revision identifiers, used by Alembic.
revision = '93c6695f7f'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('notice')
    op.drop_table('post')
    op.drop_table('reservation')
    op.drop_table('qna')
    op.drop_table('content_time')
    op.drop_table('human')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('human',
    sa.Column('human_id', sa.INTEGER(), server_default=sa.text("nextval('human_human_id_seq'::regclass)"), nullable=False),
    sa.Column('type', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('nickname', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('password', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=31), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=31), autoincrement=False, nullable=False),
    sa.Column('mobile_number', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('position', sa.VARCHAR(length=63), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('human_id', name='human_pkey'),
    sa.UniqueConstraint('email', name='human_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('content_time',
    sa.Column('content_time_id', sa.INTEGER(), server_default=sa.text("nextval('content_time_content_time_id_seq'::regclass)"), nullable=False),
    sa.Column('content_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('assigned_capacity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('note', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('minimum_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_eduticket', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_headcount', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('approved_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['content.content_id'], name='content_time_content_id_fkey'),
    sa.PrimaryKeyConstraint('content_time_id', name='content_time_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('qna',
    sa.Column('qna_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('title', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('view_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('qna_id', name='qna_pkey')
    )
    op.create_table('reservation',
    sa.Column('reservation_id', sa.INTEGER(), nullable=False),
    sa.Column('content_time_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('account_bank_code', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('account_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('account_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('deposit', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('deposit_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('manager_email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('manager_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('manager_phone', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('note', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('office_email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('organization_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('organization_type', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('payment_method', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('payment_status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('charged', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('refund', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('refund_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('refund_status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('chargeless', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vendor', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('watched_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['content_time_id'], ['content_time.content_time_id'], name='reservation_content_time_id_fkey'),
    sa.PrimaryKeyConstraint('reservation_id', name='reservation_pkey')
    )
    op.create_table('post',
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.Column('human_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('modified_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['human_id'], ['human.human_id'], name='post_human_id_fkey'),
    sa.PrimaryKeyConstraint('post_id', name='post_pkey')
    )
    op.create_table('notice',
    sa.Column('notice_id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('view_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('notice_id', name='notice_pkey')
    )
    op.create_table('event',
    sa.Column('event_id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('school', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('teacher', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('event_id', name='event_pkey')
    )
    ### end Alembic commands ###