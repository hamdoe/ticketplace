"""rename_image

Revision ID: 46dc9749ab9
Revises: 188cffd7ab1
Create Date: 2016-01-07 11:54:27.086570

"""

# revision identifiers, used by Alembic.
revision = '46dc9749ab9'
down_revision = '188cffd7ab1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('content', 'background_image', new_column_name='image_background')
    op.alter_column('content', 'main_image', new_column_name='image_main')
    op.alter_column('content', 'thumbnail_image', new_column_name='image_thumbnail')
    op.alter_column('content', 'index_image', new_column_name='image_index')



def downgrade():
    op.alter_column('content', 'image_background', new_column_name='background_image')
    op.alter_column('content', 'image_main', new_column_name='main_image')
    op.alter_column('content', 'image_thumbnail', new_column_name='thumbnail_image')
    op.alter_column('content', 'image_index', new_column_name='index_image')
