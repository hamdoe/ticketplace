"""refactor_content_dates

Revision ID: 44bea7299a8
Revises: 24999ca639b
Create Date: 2015-12-28 16:30:40.825833

"""

# revision identifiers, used by Alembic.
revision = '44bea7299a8'
down_revision = '24999ca639b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.alter_column('content', 'content_end_date', new_column_name='end_date')
    op.alter_column('content', 'content_start_date', new_column_name='start_date')


def downgrade():
    op.alter_column('content', 'end_date', new_column_name='content_end_date')
    op.alter_column('content', 'start_date', new_column_name='content_start_date')
