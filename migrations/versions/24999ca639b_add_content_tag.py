"""add content tag

Revision ID: 24999ca639b
Revises: 93c6695f7f
Create Date: 2015-12-23 14:36:49.556168

"""

# revision identifiers, used by Alembic.
revision = '24999ca639b'
down_revision = '93c6695f7f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_association',
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content.content_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('content_id', 'tag_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_association')
    op.drop_table('tag')
    ### end Alembic commands ###
