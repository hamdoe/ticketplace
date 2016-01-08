"""Data migration for content

Revision ID: 537bb869081
Revises: 195d5fc0228
Create Date: 2016-01-08 14:23:49.838116

"""

# revision identifiers, used by Alembic.

revision = '537bb869081'
down_revision = '195d5fc0228'

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column('content', 'genre',
                    existing_type=sa.INTEGER(),
                    type_=sa.Text(),
                    existing_nullable=False)


def downgrade():
    op.execute('ALTER TABLE content ALTER COLUMN genre TYPE INTEGER USING (genre::integer)')
